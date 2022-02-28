## Network

# Create Network
resource "openstack_networking_network_v2" "{{ name }}" {
  name = "{{ name }}"
}

# Create Subnet
resource "openstack_networking_subnet_v2" "{{ name ~ "_subnet" }}" {
  name            = "{{ name ~ "_subnet" }}"
  network_id      = openstack_networking_network_v2.{{ name }}.id
  cidr            = "{{ address }}"
  dns_nameservers = ["8.8.8.8", "8.8.8.4"]
}

# Attach networking port
resource "openstack_networking_port_v2" "{{ name }}" {
  name           = "{{ name }}"
  network_id     = openstack_networking_network_v2.{{ name }}.id
  admin_state_up = true
  security_group_ids = [
    {% for rule_name in rules_name %}
    openstack_compute_secgroup_v2.{{ rule_name ~ "_secgroup" }}.id,
    {% endfor %}
  ]
  fixed_ip {
    subnet_id = openstack_networking_subnet_v2.{{ name ~ "_subnet" }}.id
  }
}