"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { submitEmail, submitURL } from "@/lib/api";

type Tab = "email" | "url";

export default function SubmitPage() {
  const router = useRouter();
  const [tab, setTab] = useState<Tab>("email");
  const [file, setFile] = useState<File | null>(null);
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      let res;
      if (tab === "email") {
        if (!file) throw new Error("Please select a .eml file");
        res = await submitEmail(file);
      } else {
        if (!url.trim()) throw new Error("Please enter a URL");
        res = await submitURL(url.trim());
      }
      router.push(`/report/${res.analysis_id}`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Submission failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 560, margin: "0 auto" }}>
      <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: 8 }}>New Analysis</h1>
      <p style={{ color: "var(--muted)", marginBottom: 24 }}>Submit an email file or URL for forensic inspection.</p>

      <div className="card">
        <div style={{ display: "flex", gap: 8, marginBottom: 24 }}>
          {(["email", "url"] as Tab[]).map((t) => (
            <button
              key={t}
              className={`btn ${tab === t ? "btn-primary" : "btn-outline"}`}
              onClick={() => { setTab(t); setError(""); }}
              type="button"
              style={{ flex: 1, justifyContent: "center" }}
            >
              {t === "email" ? "📧 Email (.eml)" : "🔗 URL"}
            </button>
          ))}
        </div>

        <form onSubmit={handleSubmit}>
          {tab === "email" ? (
            <div>
              <label style={{ display: "block", marginBottom: 8, color: "var(--muted)" }}>Upload .eml file (max 5 MB)</label>
              <input
                type="file"
                accept=".eml,message/rfc822"
                onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                className="input"
                style={{ padding: 8 }}
              />
              {file && <p style={{ marginTop: 8, color: "var(--muted)", fontSize: 12 }}>{file.name} — {(file.size / 1024).toFixed(1)} KB</p>}
            </div>
          ) : (
            <div>
              <label style={{ display: "block", marginBottom: 8, color: "var(--muted)" }}>URL to inspect</label>
              <input
                type="text"
                className="input"
                placeholder="https://example.com"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
              <p style={{ marginTop: 6, fontSize: 12, color: "var(--muted)" }}>https:// is added automatically if omitted.</p>
            </div>
          )}

          {error && <p style={{ marginTop: 12, color: "var(--phishing)", fontSize: 13 }}>{error}</p>}

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            style={{ marginTop: 20, width: "100%", justifyContent: "center" }}
          >
            {loading ? "Submitting…" : "Analyze"}
          </button>
        </form>
      </div>
    </div>
  );
}
