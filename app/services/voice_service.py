"""Voice pipeline: Whisper (free STT), Amazon Polly (TTS)."""

import os
import tempfile
from typing import Optional

from app.config import get_settings

settings = get_settings()

# Optional: Google STT encoding map (when using Google)
_STT_ENCODING_MAP = {
    "audio/wav": ("LINEAR16", 16000),
    "audio/wave": ("LINEAR16", 16000),
    "audio/x-wav": ("LINEAR16", 16000),
    "audio/webm": ("WEBM_OPUS", 48000),
    "audio/webm;codecs=opus": ("WEBM_OPUS", 48000),
    "audio/ogg": ("OGG_OPUS", 48000),
    "audio/ogg;codecs=opus": ("OGG_OPUS", 48000),
    "audio/flac": ("FLAC", 16000),
}


def _speech_to_text_whisper(
    audio_bytes: bytes,
    language_code: str = "en",
    content_type: Optional[str] = None,
) -> str:
    """
    Free local STT using faster-whisper. No API key or billing.
    Supports WAV, MP3, WebM, OGG, FLAC, etc.
    """
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise RuntimeError(
            "faster-whisper not installed. Run: pip install faster-whisper"
        )

    # Map language code (e.g. en-IN -> en, hi-IN -> hi)
    lang = (language_code or "en").split("-")[0] if language_code else "en"
    if lang not in ("en", "hi", "ta", "te", "mr", "bn", "gu", "kn", "ml", "pa"):
        lang = "en"

    # Use "base" model: good balance of speed and accuracy (tiny is faster but less accurate)
    model_size = settings.whisper_model_size or "base"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    suffix = ".wav"
    if content_type:
        ct = (content_type or "").split(";")[0].strip().lower()
        if "webm" in ct:
            suffix = ".webm"
        elif "ogg" in ct:
            suffix = ".ogg"
        elif "mp3" in ct or "mpeg" in ct:
            suffix = ".mp3"
        elif "flac" in ct:
            suffix = ".flac"

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        f.write(audio_bytes)
        path = f.name

    try:
        segments, info = model.transcribe(path, language=lang, beam_size=1)
        transcript = " ".join(s.text for s in segments if s.text).strip()
        return transcript
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def _speech_to_text_google(
    audio_bytes: bytes,
    language_code: str = "en-IN",
    content_type: Optional[str] = None,
) -> str:
    """Google Speech-to-Text (requires billing + service account)."""
    try:
        from google.cloud import speech
    except ImportError:
        raise RuntimeError(
            "google-cloud-speech not installed. Run: pip install google-cloud-speech"
        )

    creds_path = settings.google_application_credentials
    if creds_path and os.path.isfile(creds_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)

    enc_name, sample_rate = _STT_ENCODING_MAP.get(
        (content_type or "").split(";")[0].strip().lower(),
        ("LINEAR16", 16000),
    )
    enc_enum = getattr(speech.RecognitionConfig.AudioEncoding, enc_name, None)
    if enc_enum is None:
        enc_enum = speech.RecognitionConfig.AudioEncoding.LINEAR16
        sample_rate = 16000

    config = speech.RecognitionConfig(
        encoding=enc_enum,
        sample_rate_hertz=sample_rate,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )

    response = client.recognize(config=config, audio=audio)
    transcript = "".join(
        r.alternatives[0].transcript for r in response.results if r.alternatives
    )
    return transcript.strip()


def speech_to_text(
    audio_bytes: bytes,
    language_code: str = "en-IN",
    content_type: Optional[str] = None,
) -> str:
    """
    Convert speech to text.
    Uses Whisper (free, local) by default. Set STT_PROVIDER=google and
    GOOGLE_APPLICATION_CREDENTIALS to use Google instead.
    """
    provider = (settings.stt_provider or "whisper").lower()

    if provider == "google" and settings.google_application_credentials and os.path.isfile(settings.google_application_credentials):
        return _speech_to_text_google(audio_bytes, language_code, content_type)
    return _speech_to_text_whisper(audio_bytes, language_code, content_type)


def text_to_speech(
    text: str,
    voice_id: Optional[str] = None,
    language_code: str = "en-IN",
    output_format: str = "mp3",
) -> bytes:
    """
    Convert text to speech using Amazon Polly.
    Returns raw audio bytes (mp3 by default).
    """
    import boto3

    voice_id = voice_id or settings.polly_voice_id

    _voice_map = {
        "hi": "Aditi",
        "hi-IN": "Aditi",
        "en": "Joanna",
        "en-IN": "Joanna",
        "en-US": "Joanna",
        "ta": "Karthik",
        "ta-IN": "Karthik",
        "te": "Karthik",
        "mr": "Aditi",
    }
    voice_id = _voice_map.get(language_code, voice_id)

    client = boto3.client(
        "polly",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )

    try:
        response = client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id,
            Engine="neural",
        )
    except Exception:
        response = client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id,
        )

    return response["AudioStream"].read()
