terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 2.65"
    }
  }

  required_version = ">= 0.14.9"
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "TerraformTesting"
  location = "eastus" ## REQUIRED
}

## VIRTUAL NETWORK
resource "azurerm_virtual_network" "vnet" {
  name                = "vNet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_subnet" "subnet" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes       = ["10.0.2.0/24"]
}

## WORDPRESS PUBLIC IP
resource "azurerm_public_ip" "wordpress_public_ip" {
  name = "wordpress_public_ip"
  location = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method = "Dynamic" ##REQUIRED??
  sku = "Basic"
}

## WORDPRESS NETWORK INTERFACE
resource "azurerm_network_interface" "wordpress_nic" {
  name                = "wordpress_nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "ipconfig1"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id = azurerm_public_ip.wordpress_public_ip.id
  }
}

## WORDPRESS VM
resource "azurerm_linux_virtual_machine" "wordpress" { ## REQUIRED
  resource_group_name = azurerm_resource_group.rg.name
  ## instance details
  name                = "wordpress-machine"
  location            = azurerm_resource_group.rg.location
  size                = "Standard_B1s" ## REQUIRED
  ## administrator account
  admin_username      = "adminuser"
  admin_password      = "P@$$w0rd1234!" ##For Bastion Connection
  disable_password_authentication = false
  #availability_set_id = azurerm_availability_set.DemoAset.id
  network_interface_ids = [
    azurerm_network_interface.wordpress_nic.id
  ]

  os_disk {
    caching              = "None"
    storage_account_type = "Standard_LRS" ## REQUIRED
  }

  admin_ssh_key {
    username = "adminuser"
    public_key = file("${path.module}/ssh_keys/wordpress_rsa.pub")
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}

## MYSQL NETWORK INTERFACE
resource "azurerm_network_interface" "mysql_nic" {
  name                = "mysql_nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
  }
}

## MYSQL VM
resource "azurerm_linux_virtual_machine" "mysql" { ## REQUIRED
  resource_group_name = azurerm_resource_group.rg.name
  ## instance details
  name                = "mysql-machine"
  location            = azurerm_resource_group.rg.location
  size                = "Standard_B1s" ## REQUIRED
  ## administrator account
  admin_username      = "adminuser"
  admin_password      = "P@$$w0rd1234!"
  disable_password_authentication = false
  #availability_set_id = azurerm_availability_set.DemoAset.id
  network_interface_ids = [
    azurerm_network_interface.mysql_nic.id
  ]

  os_disk {
    caching              = "None"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}
