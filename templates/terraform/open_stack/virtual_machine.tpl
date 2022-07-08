# Create virtual machine
resource "openstack_compute_instance_v2" "{{ infra_element_name }}" {
  name        = "{{ vm_name }}"
  image_name  = "{{ os }}"
  flavor_name = "{{ vm_flavor }}"
  key_pair    = openstack_compute_keypair_v2.{{ vm_key_name }}.name
  network {
    port = openstack_networking_port_v2.{{ i1.belongsTo }}.id
  }

  ## AGENTS TO ADD
  # this is subject to be moved to IEM as part of its baseline
    provisioner "local-exec" {
    command = "ansible-galaxy collection install community.general"
  }

  # this is subject to be moved to IEM as part of its baseline
  provisioner "local-exec" {
    command = "ansible-playbook ansible/playbooks/pma/site_requirements.yaml"
  }

  # secrets can be taken from environment variables at IEM but these security issues I will leave them to y2, the user can also be problematic ubuntu/root/centos/...
  provisioner "local-exec" {
    command = "ansible-playbook -u root -i '${openstack_networking_floatingip_v2.{{ infra_element_name ~ "_floating_ip"}}.address},' ansible/playbooks/pma/site.yaml --extra-vars '{\"pma_deployment_id\": \"123e4567-e89b-12d3-a456-426614174002\", \"pma_influxdb_bucket\": \"bucket\", \"pma_influxdb_token\": \"piacerePassword\", \"pma_influxdb_org\": \"piacere\", \"pma_influxdb_addr\": \"https://influxdb.pm.ci.piacere.digital.tecnalia.dev\" }'"
  }

}

# Create ssh keys
resource "openstack_compute_keypair_v2" "{{ vm_key_name }}" {
  name       = "{{ vm_key_name }}"
  # public_key = "{{ ssh_key_file }}"
}

# Create floating ip
resource "openstack_networking_floatingip_v2" "{{infra_element_name ~ "_floating_ip"}}" {
  pool = "external"
  # fixed_ip = "{{ address }}"
}

# Attach floating ip to instance
resource "openstack_compute_floatingip_associate_v2" "{{ infra_element_name ~ "_floating_ip_association" }}" {
  floating_ip = openstack_networking_floatingip_v2.{{ infra_element_name ~ "_floating_ip" }}.address
  instance_id = openstack_compute_instance_v2.{{ infra_element_name }}.id
}
