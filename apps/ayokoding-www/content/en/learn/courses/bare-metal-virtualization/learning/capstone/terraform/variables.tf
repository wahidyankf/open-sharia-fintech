# => Has no default because a real Proxmox endpoint is environment-specific and should not be committed here.
variable "proxmox_endpoint" {
  type      = string
  sensitive = true
}

# => Receives an owner-provided short-lived API token via a secure environment or secret manager.
variable "proxmox_api_token" {
  type      = string
  sensitive = true
}

# => Makes environment labels explicit without embedding an address, disk, or guest identity in the course.
variable "environment" {
  type    = string
  default = "lab"
}
