export type Verdict = "SAFE" | "MARKETING" | "SUSPICIOUS" | "PHISHING";
export type AnalysisStatus = "pending" | "running" | "complete" | "failed";
export type AnalysisType = "email" | "url";

export interface AnalysisSummary {
  analysis_id: string;
  type: AnalysisType;
  target: string;
  status: AnalysisStatus;
  verdict: Verdict | null;
  score: number | null;
  created_at: string;
}

export interface Feature {
  feature: string;
  weight: number;
}

export interface Report {
  analysis_id: string;
  type: AnalysisType;
  target: string;
  verdict: Verdict;
  score: number;
  completed_at: string;
  pipeline: Record<string, unknown>;
  top_features: Feature[];
  iocs: {
    ips: string[];
    domains: string[];
    urls: string[];
    emails: string[];
  };
  error: string | null;
}
