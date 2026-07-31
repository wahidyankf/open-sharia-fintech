module "dev" {
  source      = "./modules/service"
  environment = "dev"
}

module "stage" {
  source      = "./modules/service"
  environment = "stage"
}
output "names" { value = [module.dev.name, module.stage.name] }
