# => This is an image contract only; an owner supplies ISO checksums and Proxmox connection values out of band.
packer {
  required_plugins {
    # => Pins the plugin source in a real reviewed build; choose and verify a current version before use.
    proxmox = { source = "github.com/hashicorp/proxmox" }
  }
}

# => Keeps generic guest readiness in the image, not per-environment secrets or addresses.
build {
  name    = "cloud-init-ready-template"
  sources = ["source.proxmox-iso.lab_template"]
}
