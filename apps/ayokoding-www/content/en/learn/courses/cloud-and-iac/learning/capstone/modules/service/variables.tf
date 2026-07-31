variable "environment" {
  description = "The reviewed environment name used in resource names and tags."
  type        = string
}

variable "owner" {
  description = "The accountable team label, not a personal credential or identifier."
  type        = string
  default     = "learning-team"
}

variable "cost_center" {
  description = "The cost allocation label used by the learning environment."
  type        = string
  default     = "training"
}
