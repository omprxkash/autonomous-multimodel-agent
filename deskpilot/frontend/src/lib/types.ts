export interface User {
  id: string;
  email: string;
  name: string;
  picture: string | null;
  personalization: string;
}

export interface Conversation {
  id: string;
  title: string;
  updated_at: string;
}

export interface Message {
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export interface SendResponse {
  conversation_id: string;
  reply: string;
  has_draft: boolean;
}
