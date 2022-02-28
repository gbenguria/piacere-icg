## VIRTUAL NETWORK
resource "azurerm_virtual_network" "{{ name ~ "_vnetwork" }}" {
  name                = "{{ name }}"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.{{ resource_group_name }}.location
  resource_group_name = azurerm_resource_group.{{ resource_group_name }}.name
}

## SUBNET
resource "azurerm_subnet" "{{ name ~ "_subnet" }}" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.{{ resource_group_name }}.name
  virtual_network_name = azurerm_virtual_network.{{ name ~ "_vnetwork" }}.name
  address_prefixes       = ["10.0.2.0/24"]
}