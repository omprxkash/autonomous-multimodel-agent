import { AnalysisSummary, Report } from "./types";

const BASE = "/api/v1";

export async function submitEmail(file: File): Promise<{ analysis_id: string }> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE}/analyze/email`, { method: "POST", body: form });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function submitURL(url: string): Promise<{ analysis_id: string }> {
  const res = await fetch(`${BASE}/analyze/url`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function pollStatus(id: string): Promise<AnalysisSummary> {
  const res = await fetch(`${BASE}/analysis/${id}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getReport(id: string): Promise<Report> {
  const res = await fetch(`${BASE}/report/${id}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function listAnalyses(): Promise<AnalysisSummary[]> {
  const res = await fetch(`${BASE}/analyses`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export function exportUrl(id: string, format: "json" | "csv" | "stix2"): string {
  return `${BASE}/report/${id}/export?format=${format}`;
}
