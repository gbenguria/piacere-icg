output "resource_group_id" {
  value = azurerm_resource_group.rg.id
}

output "wordpress_public_ip" {
  value = azurerm_public_ip.wordpress_public_ip.ip_address
}

output "wordpress_dns_name" {
  value = azurerm_public_ip.wordpress_public_ip.name
}
