const BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export interface Lead {
  id: string;
  company: string;
  domain: string;
  industry: string | null;
  employee_count: number | null;
  location: string | null;
  contact_name: string | null;
  title: string | null;
  email: string | null;
  tech_stack: string[];
  score: number | null;
  score_breakdown: Record<string, FactorBreakdown> | null;
  email_draft: string | null;
  stage: string;
  created_at: string | null;
}

export interface FactorBreakdown {
  points: number;
  max: number;
  matched?: boolean | string[];
  value?: string | number | string[] | null;
  bucket?: string;
}

export interface PipelineRunResponse {
  processed: number;
  leads: Lead[];
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`${res.status}: ${body}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  getLeads: (stage?: string, minScore?: number) => {
    const params = new URLSearchParams();
    if (stage) params.set("stage", stage);
    if (minScore !== undefined) params.set("min_score", String(minScore));
    const qs = params.toString();
    return request<Lead[]>(`/leads${qs ? `?${qs}` : ""}`);
  },

  getLead: (id: string) => request<Lead>(`/leads/${id}`),

  updateStage: (id: string, stage: string) =>
    request<Lead>(`/leads/${id}/stage`, {
      method: "PATCH",
      body: JSON.stringify({ stage }),
    }),

  runPipeline: (mock = true) =>
    request<PipelineRunResponse>("/pipeline/run", {
      method: "POST",
      body: JSON.stringify({ mock }),
    }),
};

