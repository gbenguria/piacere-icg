## Network

# Create Network
resource "openstack_networking_network_v2" "{{ infra_element_name }}" {
  name = "{{ name }}"
}

# Create Subnet
resource "openstack_networking_subnet_v2" "{{ infra_element_name ~ "_subnet" }}" {
  name            = "{{ name ~ "_subnet" }}"
  network_id      = openstack_networking_network_v2.{{ infra_element_name }}.id
  cidr            = "{{ addressRange }}"
  dns_nameservers = ["8.8.8.8", "8.8.8.4"]
}

# Attach networking port
resource "openstack_networking_port_v2" "{{ infra_element_name }}" {
  name           = "{{ name }}"
  network_id     = openstack_networking_network_v2.{{ infra_element_name }}.id
  admin_state_up = true
  security_group_ids = [
    data.openstack_networking_secgroup_v2.default.id        #default flavour id
  ]
  fixed_ip {
    subnet_id = openstack_networking_subnet_v2.{{ infra_element_name ~ "_subnet" }}.id
  }
}

# Create router
resource "openstack_networking_router_v2" "{{ infra_element_name ~ "_router" }}" {
  name                = "{{ infra_element_name ~ "_router" }}"
  external_network_id = data.openstack_networking_network_v2.external.id    #External network id
}
# Router interface configuration
resource "openstack_networking_router_interface_v2" "{{ infra_element_name ~ "_router_interface" }}" {
  router_id = openstack_networking_router_v2.{{ infra_element_name ~ "_router" }}.id
  subnet_id = openstack_networking_subnet_v2.{{ infra_element_name ~ "_subnet" }}.id
}