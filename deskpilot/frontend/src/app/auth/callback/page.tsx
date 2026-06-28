"use client";

import { useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";

export default function AuthCallback() {
  const params = useSearchParams();
  const router = useRouter();

  useEffect(() => {
    const token = params.get("token");
    const userId = params.get("user_id");
    const isSetupComplete = params.get("is_setup_complete");
    const warning = params.get("warning");

    if (token) {
      localStorage.setItem("dp_token", token);
      if (userId) localStorage.setItem("dp_user_id", userId);
      if (isSetupComplete !== null) localStorage.setItem("dp_setup", isSetupComplete);
      if (warning) localStorage.setItem("dp_warning", decodeURIComponent(warning));
      router.replace("/");
    } else {
      router.replace("/?error=auth_failed");
    }
  }, [params, router]);

  return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "100vh", color: "var(--muted)" }}>
      Signing you in...
    </div>
  );
}
