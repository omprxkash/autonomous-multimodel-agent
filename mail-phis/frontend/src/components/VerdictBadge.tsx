import { Verdict } from "@/lib/types";

export default function VerdictBadge({ verdict }: { verdict: Verdict }) {
  const cls: Record<Verdict, string> = {
    SAFE: "badge badge-safe",
    MARKETING: "badge badge-marketing",
    SUSPICIOUS: "badge badge-suspicious",
    PHISHING: "badge badge-phishing",
  };
  return <span className={cls[verdict]}>{verdict}</span>;
}
