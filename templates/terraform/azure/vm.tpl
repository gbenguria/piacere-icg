terraform {
  required_providers {
    azurerm = {
      source = "{{ source }}"
      version = "{{ version }}"
    }
  }
}
provider "azurerm" {
  features {}
}
resource "azurerm_resource_group" "rg" {
  name = "{{ name }}"
  location = "{{ location }}"
}