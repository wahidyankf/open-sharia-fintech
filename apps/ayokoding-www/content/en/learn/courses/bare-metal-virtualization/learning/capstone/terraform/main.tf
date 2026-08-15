# => Selects the maintained Proxmox provider; confirm its current version and checksum in an owner-reviewed lock file.
terraform {
  required_providers {
    proxmox = {
      source = "bpg/proxmox"
    }
  }
}

# => Deliberately receives endpoint and token from secure input; neither value has a repository default.
provider "proxmox" {
  endpoint  = var.proxmox_endpoint
  api_token = var.proxmox_api_token
  insecure  = false
}

# => Documents intended clone inputs without a resource block that could create a guest when copied blindly.
locals {
  guest_contract = {
    environment = var.environment
    template    = "owner-approved-cloud-init-template"
    storage     = "owner-approved-redundant-storage"
  }
}
