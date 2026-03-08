"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login, register, ApiError } from "@/lib/api";
import { useAuthStore } from "@/store/authStore";

type Tab = "login" | "register";

export default function LoginPage() {
  const router = useRouter();
  const setAuth = useAuthStore((s) => s.setAuth);

  const [tab, setTab] = useState<Tab>("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data =
        tab === "login"
          ? await login({ email, password })
          : await register({ email, password, name: name || undefined });

      setAuth(data.user_id, data.email, data.token);
      router.push("/chat");
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.detail ?? err.message);
      } else {
        setError("Something went wrong");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex h-screen">
      {/* ── Left panel (indigo) ── */}
      <div className="hidden md:flex w-2/5 bg-[#1A1560] flex-col items-center justify-center text-white px-10">
        <h1 className="text-5xl font-bold tracking-tight">SETU</h1>
        <p className="mt-4 text-lg text-white/70 text-center leading-relaxed">
          सरकारी योजनाओं तक आपका सेतु
        </p>
      </div>

      {/* ── Right panel (form) ── */}
      <div className="flex-1 flex items-center justify-center bg-[#FAFAF8] px-6">
        <div className="w-full max-w-sm space-y-6">
          {/* Tab switcher */}
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setTab("login")}
              className={`flex-1 pb-2 text-sm font-medium transition-colors ${
                tab === "login"
                  ? "border-b-2 border-[#E8610A] text-[#E8610A]"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              लॉगिन
            </button>
            <button
              onClick={() => setTab("register")}
              className={`flex-1 pb-2 text-sm font-medium transition-colors ${
                tab === "register"
                  ? "border-b-2 border-[#E8610A] text-[#E8610A]"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            >
              रजिस्टर
            </button>
          </div>

          {/* Error */}
          {error && (
            <p className="text-sm text-red-600 bg-red-50 rounded-lg px-3 py-2">
              {error}
            </p>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {tab === "register" && (
              <input
                type="text"
                placeholder="नाम"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm outline-none focus:border-[#1A1560] focus:ring-1 focus:ring-[#1A1560]"
              />
            )}

            <input
              type="email"
              required
              placeholder="ईमेल"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm outline-none focus:border-[#1A1560] focus:ring-1 focus:ring-[#1A1560]"
            />

            <input
              type="password"
              required
              placeholder="पासवर्ड"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm outline-none focus:border-[#1A1560] focus:ring-1 focus:ring-[#1A1560]"
            />

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-[#E8610A] py-2.5 text-sm font-medium text-white hover:bg-[#d15709] disabled:opacity-50 transition-colors"
            >
              {loading
                ? "..."
                : tab === "login"
                  ? "लॉगिन करें"
                  : "रजिस्टर करें"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
