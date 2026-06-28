"use client";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("dp_token");
}

export function setToken(token: string) {
  localStorage.setItem("dp_token", token);
}

export function clearToken() {
  localStorage.removeItem("dp_token");
}

export function isAuthenticated(): boolean {
  return !!getToken();
}

export function loginWithGoogle() {
  window.location.href = "/api/auth/login";
}
