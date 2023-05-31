

output "instance_server_public_key_ubuntu_nginx_vm" {
  value = openstack_compute_keypair_v2.ubuntu.public_key
}

output "instance_server_private_key_ubuntu_nginx_vm" {
  value = openstack_compute_keypair_v2.ubuntu.private_key
}

output "instance_server_public_ip_nginx_vm" {
  value = openstack_compute_floatingip_associate_v2.nginx_vm_floating_ip_association.floating_ip
}

