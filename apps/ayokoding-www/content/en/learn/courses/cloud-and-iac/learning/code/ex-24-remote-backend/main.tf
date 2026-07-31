terraform {
  # This is deliberately local: it can initialize without an account or network service.
  backend "local" {
    path = "terraform.tfstate.example"
  }
}
