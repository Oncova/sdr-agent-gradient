# ──────────────────────────────────────────────────────────
# Terraform Provider Configuration — DigitalOcean + Vault
# ──────────────────────────────────────────────────────────

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.34"
    }
    vault = {
      source  = "hashicorp/vault"
      version = "~> 4.2"
    }
  }

  backend "local" {
    path = "terraform.tfstate"
  }
}

provider "digitalocean" {
  token = var.do_token
}

provider "vault" {
  address = var.vault_addr
  token   = var.vault_token
}

# ──────────────────────────────────────────────────────────
# DigitalOcean Droplet — n8n Orchestrator
# ──────────────────────────────────────────────────────────

resource "digitalocean_droplet" "n8n_orchestrator" {
  image    = "docker-20-04"
  name     = "sdr-n8n-orchestrator"
  region   = "nyc3"
  size     = "s-2vcpu-4gb"
  ssh_keys = var.ssh_key_ids

  user_data = <<-EOF
    #!/bin/bash
    set -euo pipefail
    apt-get update -y && apt-get install -y docker-compose
    mkdir -p /opt/n8n && cd /opt/n8n
    cat > docker-compose.yml <<'COMPOSE'
    version: "3.8"
    services:
      n8n:
        image: n8nio/n8n:latest
        restart: always
        ports:
          - "5678:5678"
        environment:
          - N8N_BASIC_AUTH_ACTIVE=true
          - N8N_BASIC_AUTH_USER=${var.n8n_user}
          - N8N_BASIC_AUTH_PASSWORD=${var.n8n_password}
          - WEBHOOK_URL=https://${var.n8n_domain}
        volumes:
          - n8n_data:/home/node/.n8n
    volumes:
      n8n_data:
    COMPOSE
    docker-compose up -d
  EOF

  tags = ["sdr-army", "n8n", "production"]
}

# ──────────────────────────────────────────────────────────
# DigitalOcean Firewall — Lock down n8n
# ──────────────────────────────────────────────────────────

resource "digitalocean_firewall" "n8n_firewall" {
  name        = "sdr-n8n-firewall"
  droplet_ids = [digitalocean_droplet.n8n_orchestrator.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = var.allowed_ssh_ips
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "5678"
    source_addresses = var.allowed_ssh_ips
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}

# ──────────────────────────────────────────────────────────
# Vault Secret Paths — Pre-seed structure
# ──────────────────────────────────────────────────────────

resource "vault_mount" "enterprise_revops" {
  path        = "enterprise-revops"
  type        = "kv"
  options     = { version = "2" }
  description = "SDR Army operational secrets"
}

resource "vault_generic_secret" "google_workspace" {
  path = "enterprise-revops/data/google_workspace"
  data_json = jsonencode({
    service_account_json = var.gcp_service_account_json
    admin_inbox          = "revops@yourdomain.com"
  })
  depends_on = [vault_mount.enterprise_revops]
}

resource "vault_generic_secret" "brightdata" {
  path = "enterprise-revops/data/brightdata"
  data_json = jsonencode({
    account_id = var.bd_account_id
    api_token  = var.bd_api_token
    username   = var.bd_username
    password   = var.bd_password
  })
  depends_on = [vault_mount.enterprise_revops]
}

resource "vault_generic_secret" "elevenlabs" {
  path = "enterprise-revops/data/elevenlabs"
  data_json = jsonencode({
    api_key  = var.elevenlabs_api_key
    voice_id = var.elevenlabs_voice_id
  })
  depends_on = [vault_mount.enterprise_revops]
}

resource "vault_generic_secret" "n8n_orchestration" {
  path = "enterprise-revops/data/n8n_orchestration"
  data_json = jsonencode({
    base_url = "https://${var.n8n_domain}"
    api_key  = var.n8n_api_key
  })
  depends_on = [vault_mount.enterprise_revops]
}
