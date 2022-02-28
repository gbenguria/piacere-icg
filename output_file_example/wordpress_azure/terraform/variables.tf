variable "resource_group_name" {
  default = "rg"
  type = string
}

### VMs

variable "small_vm" {
    type = object({
        name = string,
        location = string,
        size = string,
        admin_username = string,
        admin_password = string
    })
    default = {
      admin_password = "P@$$w0rd1234!"
      admin_username = "adminuser"
      location = "eastus"
      name = "myvm"
      size = "Standard_B1s"
    }
}

### MySql

variable "mysql_vm_name" {
  type = string
  default = "MySql"
}

