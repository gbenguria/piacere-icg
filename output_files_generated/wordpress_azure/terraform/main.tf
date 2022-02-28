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

## VIRTUAL NETWORK
resource "azurerm_virtual_network" "wordpress_net_vnetwork" {
  name                = "wordpress_net"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.wordpress-example.location
  resource_group_name = azurerm_resource_group.wordpress-example.name
}

## SUBNET
resource "azurerm_subnet" "wordpress_net_subnet" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.wordpress-example.name
  virtual_network_name = azurerm_virtual_network.wordpress_net_vnetwork.name
  address_prefixes       = ["10.0.2.0/24"]
}

## VIRTUAL NETWORK
resource "azurerm_virtual_network" "mysql_net_vnetwork" {
  name                = "mysql_net"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.mysql-example.location
  resource_group_name = azurerm_resource_group.mysql-example.name
}

## SUBNET
resource "azurerm_subnet" "mysql_net_subnet" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.mysql-example.name
  virtual_network_name = azurerm_virtual_network.mysql_net_vnetwork.name
  address_prefixes       = ["10.0.2.0/24"]
}

