# ──────────────────────────────────────────────────────────
# Outputs — Post-apply reference values
# ──────────────────────────────────────────────────────────

output "n8n_droplet_ip" {
  description = "Public IP of the n8n orchestrator droplet"
  value       = digitalocean_droplet.n8n_orchestrator.ipv4_address
}

output "n8n_webhook_url" {
  description = "Base webhook URL for n8n"
  value       = "https://${var.n8n_domain}"
}

output "vault_mount_path" {
  description = "Vault KV v2 mount path for SDR secrets"
  value       = vault_mount.enterprise_revops.path
}
