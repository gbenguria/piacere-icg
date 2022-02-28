terraform {
required_version = ">= 0.14.0"
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.35.0"
    }
  }
}

# Configure the OpenStack Provider
provider "openstack" {
  user_name   = "admin"
  tenant_name = "test"
  password    = "wRpuXgVqBzQqGwx8Bu0sylEeb8FgjSYG"
  auth_url    = "https://127.0.0.1:5000/v3"
  insecure    = true
}