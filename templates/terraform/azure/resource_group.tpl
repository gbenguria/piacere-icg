## RESOURCE GROUP

resource "azurerm_resource_group" "{{ name }}" {
  name     = "{{ name }}"
  location = "{{ location }}" ## REQUIRED
}