# ──────────────────────────────────────────────────────────
# Variables — DigitalOcean, Vault, and Service Credentials
# ──────────────────────────────────────────────────────────

# ── DigitalOcean ──
variable "do_token" {
  description = "DigitalOcean API token"
  type        = string
  sensitive   = true
}

variable "ssh_key_ids" {
  description = "List of DigitalOcean SSH key IDs for droplet access"
  type        = list(string)
  default     = []
}

variable "allowed_ssh_ips" {
  description = "IP addresses allowed to SSH into droplets"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

# ── Vault ──
variable "vault_addr" {
  description = "HashiCorp Vault server address"
  type        = string
  default     = "http://127.0.0.1:8200"
}

variable "vault_token" {
  description = "HashiCorp Vault root/dev token"
  type        = string
  sensitive   = true
  default     = "dev-root-token"
}

# ── n8n ──
variable "n8n_domain" {
  description = "Domain for the n8n webhook endpoint"
  type        = string
  default     = "n8n.yourdomain.com"
}

variable "n8n_user" {
  description = "n8n basic auth username"
  type        = string
  default     = "admin"
}

variable "n8n_password" {
  description = "n8n basic auth password"
  type        = string
  sensitive   = true
  default     = "changeme"
}

variable "n8n_api_key" {
  description = "n8n API key for webhook triggering"
  type        = string
  sensitive   = true
  default     = ""
}

# ── Google Workspace ──
variable "gcp_service_account_json" {
  description = "GCP service account JSON (stringified)"
  type        = string
  sensitive   = true
  default     = "{}"
}

# ── Bright Data ──
variable "bd_account_id" {
  description = "Bright Data account ID"
  type        = string
  default     = ""
}

variable "bd_api_token" {
  description = "Bright Data API token"
  type        = string
  sensitive   = true
  default     = ""
}

variable "bd_username" {
  description = "Bright Data proxy username"
  type        = string
  default     = ""
}

variable "bd_password" {
  description = "Bright Data proxy password"
  type        = string
  sensitive   = true
  default     = ""
}

# ── ElevenLabs ──
variable "elevenlabs_api_key" {
  description = "ElevenLabs API key"
  type        = string
  sensitive   = true
  default     = ""
}

variable "elevenlabs_voice_id" {
  description = "ElevenLabs voice ID for pitch synthesis"
  type        = string
  default     = ""
}
