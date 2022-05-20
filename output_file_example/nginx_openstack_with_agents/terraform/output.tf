output "instance_server_public_key" {
  value = openstack_compute_keypair_v2.user_key.public_key
}

output "instance_server_private_key" {
  value = openstack_compute_keypair_v2.user_key.private_key
}