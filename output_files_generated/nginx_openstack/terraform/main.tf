terraform {
required_version = ">= 0.14.0"
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.35.0"
    }
  }
}

# Configure the OpenStack Provider
provider "openstack" {
  user_name   = var.openstack_username
  tenant_name = "admin"
  password    = var.openstack_password
  auth_url    = var.openstack_auth_url
  insecure    = true
}

# Retrieve data
data "openstack_networking_network_v2" "external" {
  name = "external"
}

data "openstack_identity_project_v3" "test_tenant" {
  name = "admin"
}

data "openstack_networking_secgroup_v2" "default" {
  name = "default"
  tenant_id = data.openstack_identity_project_v3.test_tenant.id
}
# Create virtual machine
resource "openstack_compute_instance_v2" "vm1" {
  name        = "nginx-host"
  image_name  = "ubuntu-20.04.3"
  flavor_name = "small"
  key_pair    = openstack_compute_keypair_v2.ssh_key.name
  network {
    port = openstack_networking_port_v2.net1.id
  }
}

# Create ssh keys
resource "openstack_compute_keypair_v2" "ssh_key" {
  name       = ""
  public_key = ""
}

# Create floating ip
resource "openstack_networking_floatingip_v2" "vm1_floating_ip" {
  pool = "external"
  # fixed_ip = ""
}

# Attach floating ip to instance
resource "openstack_compute_floatingip_associate_v2" "vm1_floating_ip_association" {
  floating_ip = openstack_networking_floatingip_v2.vm1_floating_ip.address
  instance_id = openstack_compute_instance_v2.vm1.id
}

## Network

# Create Network
resource "openstack_networking_network_v2" "net1" {
  name = "ostack2"
}

# Create Subnet
resource "openstack_networking_subnet_v2" "net1_subnet" {
  name            = "ostack2_subnet"
  network_id      = openstack_networking_network_v2.net1.id
  cidr            = "16.0.0.0/24"
  dns_nameservers = ["8.8.8.8", "8.8.8.4"]
}

# Attach networking port
resource "openstack_networking_port_v2" "net1" {
  name           = "ostack2"
  network_id     = openstack_networking_network_v2.net1.id
  admin_state_up = true
  security_group_ids = [
    data.openstack_networking_secgroup_v2.default.id        #default flavour id
  ]
  fixed_ip {
    subnet_id = openstack_networking_subnet_v2.net1_subnet.id
  }
}

# Create router
resource "openstack_networking_router_v2" "net1_router" {
  name                = "net1_router"
  external_network_id = data.openstack_networking_network_v2.external.id    #External network id
}
# Router interface configuration
resource "openstack_networking_router_interface_v2" "net1_router_interface" {
  router_id = openstack_networking_router_v2.net1_router.id
  subnet_id = openstack_networking_subnet_v2.net1_subnet.id
}

