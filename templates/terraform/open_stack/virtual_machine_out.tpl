output "instance_server_public_key_{{ vm_key_name }}" {
  value = openstack_compute_keypair_v2.{{ vm_key_name }}.public_key
}

output "instance_server_private_key_{{ vm_key_name }}" {
  value = openstack_compute_keypair_v2.{{ vm_key_name }}.private_key
}

output "instance_ip_{{ vm_name }}" {
  value = openstack_compute_floatingip_associate_v2.{{ infra_element_name ~ "_floating_ip_association" }}.floating_ip
}