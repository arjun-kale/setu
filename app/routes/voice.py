"""Voice API: POST /api/voice — audio upload → STT → chat → TTS → return audio."""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from app.services.ai_agent import get_ai_response
from app.services.dynamodb_service import DynamoDBService, get_dynamodb_service
from app.services.voice_service import speech_to_text, text_to_speech

router = APIRouter()


@router.post("/voice")
def voice(
    audio: UploadFile = File(..., description="Audio file (WAV, WebM, OGG, FLAC)"),
    user_id: str = Form(default="voice-user", description="User identifier"),
    language: str = Form(default="en-IN", description="Language code (e.g. en-IN, hi-IN)"),
    dynamo: DynamoDBService = Depends(get_dynamodb_service),
):
    """
    Voice assistant endpoint.
    1. Accept audio upload
    2. Convert speech to text (Google Speech-to-Text)
    3. Send text to chat service
    4. Convert response to speech (Amazon Polly)
    5. Return audio file (MP3)
    """
    # 1. Read audio bytes
    audio_bytes = audio.file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio file")

    content_type = audio.content_type or ""

    # 2. Speech to text
    try:
        transcript = speech_to_text(
            audio_bytes,
            language_code=language or "en-IN",
            content_type=content_type,
        )
    except RuntimeError as e:
        if "not installed" in str(e):
            raise HTTPException(
                status_code=503,
                detail="Speech-to-Text not available. Run: pip install faster-whisper",
            ) from e
        raise HTTPException(status_code=500, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech-to-text failed: {e}") from e

    if not transcript:
        raise HTTPException(
            status_code=400,
            detail="Could not transcribe audio. Ensure clear speech and supported format (WAV, WebM, OGG, FLAC).",
        )

    # 3. Send to chat service (same logic as POST /api/chat)
    user_id = (user_id or "voice-user").strip()
    session_id = user_id
    language = (language or "en-IN").strip()

    if dynamo.get_user(user_id) is None:
        dynamo.create_user(user_id)
    dynamo.create_session(session_id, user_id=user_id)
    dynamo.save_message(session_id, "user", transcript)

    chat_history = dynamo.get_chat_history(session_id, limit=10)
    ai_response = get_ai_response(
        transcript,
        language=language,
        session_id=session_id,
        user_id=user_id,
        chat_history=chat_history,
    )

    dynamo.save_message(session_id, "assistant", ai_response)

    # 4. Text to speech
    try:
        audio_out = text_to_speech(
            ai_response,
            language_code=language,
            output_format="mp3",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text-to-speech failed: {e}") from e

    # 5. Return audio file
    return Response(
        content=audio_out,
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": "attachment; filename=response.mp3",
            "X-Transcript": transcript[:200],  # Optional: echo back transcript
            "X-Response-Text": ai_response[:200],  # Optional: echo back response text
        },
    )
