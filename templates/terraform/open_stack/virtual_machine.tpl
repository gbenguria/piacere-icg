# Create virtual machine
resource "openstack_compute_instance_v2" "{{ name }}" {
  name        = "{{ name }}"
  image_name  = "{{ image }}"
  flavor_name = "{{ flavor }}"
  key_pair    = openstack_compute_keypair_v2.{{ name ~ "_ssh_key" }}.name
  network {
    port = openstack_networking_port_v2.{{ network_name }}.id
  }
}

# Create ssh keys
resource "openstack_compute_keypair_v2" "{{ name ~ "_ssh_key" }}" {
  name       = "{{ ssh_user }}"
  public_key = "{{ ssh_key_file }}"
}

# Create floating ip
resource "openstack_networking_floatingip_v2" "{{name ~ "_floating_ip"}}" {
  pool = "external"
  # fixed_ip = "{{ address }}"
}

# Attach floating ip to instance
resource "openstack_compute_floatingip_associate_v2" "{{ name ~ "_floating_ip_association" }}" {
  floating_ip = openstack_networking_floatingip_v2.{{ name ~ "_floating_ip" }}.address
  instance_id = openstack_compute_instance_v2.{{ name }}.id
}
