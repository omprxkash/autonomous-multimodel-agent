import { Conversation, Message, SendResponse, User } from "./types";

const BASE = "/api";

function authHeaders(): HeadersInit {
  const token = typeof window !== "undefined" ? localStorage.getItem("dp_token") : null;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function getMe(): Promise<User> {
  const res = await fetch(`${BASE}/auth/me`, { headers: authHeaders() });
  if (!res.ok) throw new Error("Not authenticated");
  return res.json();
}

export async function listConversations(): Promise<Conversation[]> {
  const res = await fetch(`${BASE}/chat/conversations`, { headers: authHeaders() });
  if (!res.ok) throw new Error("Failed to load conversations");
  return res.json();
}

export async function getMessages(convId: string): Promise<Message[]> {
  const res = await fetch(`${BASE}/chat/conversations/${convId}/messages`, { headers: authHeaders() });
  if (!res.ok) throw new Error("Failed to load messages");
  return res.json();
}

export async function sendMessage(message: string, conversationId?: string): Promise<SendResponse> {
  const res = await fetch(`${BASE}/chat/message`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ message, conversation_id: conversationId }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
