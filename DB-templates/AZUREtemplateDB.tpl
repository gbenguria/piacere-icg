resource "azurerm_sql_database" "test2" {
  name                = "{{ name }}"
  resource_group_name = "{{ group_name}}"
  location            = "{{ location }}"
  server_name         = "{{ server_name  }}"

  threat_detection_policy {
    state                      = "{{ state }}"
    email_addresses            = {{ email }}
    retention_days             = "{{ days }}"
    storage_account_access_key = "{{ access_key }}"
    storage_endpoint           = "{{ endpoint }}"
    use_server_default         = "{{ default }}"
  }
}