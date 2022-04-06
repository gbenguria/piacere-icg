# Create virtual machine
resource "openstack_compute_instance_v2" "{{ infra_element_name }}" {
  name        = "{{ vm_name }}"
  image_name  = "{{ i1.name }}"
  flavor_name = "{{ vm_flavor }}"
  key_pair    = openstack_compute_keypair_v2.{{ credentials }}.name
  network {
    port = openstack_networking_port_v2.{{ i1.belongsTo }}.id
  }
}

# Create ssh keys
resource "openstack_compute_keypair_v2" "{{ credentials }}" {
  name       = "{{ ssh_user }}"
  public_key = "{{ ssh_key_file }}"
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
