variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "app_name" {
  description = "Application name (used as prefix for resource naming)"
  type        = string
  default     = "deskpilot"
}

variable "db_name" {
  description = "PostgreSQL database name"
  type        = string
  default     = "deskpilot"
}

variable "db_username" {
  description = "PostgreSQL master username"
  type        = string
  default     = "deskpilot"
}

variable "db_password" {
  description = "PostgreSQL master password"
  type        = string
  sensitive   = true
}

variable "gemini_api_key" {
  description = "Google Gemini API key"
  type        = string
  sensitive   = true
}

variable "google_client_id" {
  description = "Google OAuth 2.0 client ID"
  type        = string
}

variable "google_client_secret" {
  description = "Google OAuth 2.0 client secret"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "Application JWT secret key"
  type        = string
  sensitive   = true
}
