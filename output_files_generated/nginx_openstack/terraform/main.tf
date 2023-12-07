

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
  insecure    = true
}

# Retrieve data
data "openstack_networking_network_v2" "external" {
  name = "external"
}


## Network
# Create Network
resource "openstack_networking_network_v2" "ext_net" {
  name = "concrete_net"
}

# Create router
resource "openstack_networking_router_v2" "router_ext_net" { 
  name                = "router_ext_net"
  external_network_id = data.openstack_networking_network_v2.external.id
}


# Subnet
resource "openstack_networking_subnet_v2" "concrete_subnet_subnet" {
  name            = "concrete_subnet_subnet"
  network_id      = openstack_networking_network_v2.ext_net.id
  cidr            = "10.0.0.0/24"
  dns_nameservers = ["8.8.8.8", "8.8.8.4"]
}

# Create router interface on subnet
resource "openstack_networking_router_interface_v2" "router_interface_ext_net_concrete_subnet_subnet" {
  router_id = "${openstack_networking_router_v2.router_ext_net.id}"
  subnet_id = "${openstack_networking_subnet_v2.concrete_subnet_subnet.id}"
}




# Create ssh keys
resource "openstack_compute_keypair_v2" "ssh_key" {
  name       = "vm2user"
  # public_key = ""
}



# CREATING SECURITY_GROUP
resource "openstack_compute_secgroup_v2" "sg" {
    name = "infra_element_name"
    description = "PIACERE security group created - sg"   
    rule {
        from_port   = -1
        to_port     = -1
        ip_protocol = "icmp"
        cidr        = "0.0.0.0/0"
    } 
    rule {
        from_port   = 80
        to_port     = 80
        ip_protocol = "tcp"
        cidr        = "0.0.0.0/0"
    } 
    rule {
        from_port   = 443
        to_port     = 443
        ip_protocol = "tcp"
        cidr        = "0.0.0.0/0"
    } 
    rule {
        from_port   = 22
        to_port     = 22
        ip_protocol = "tcp"
        cidr        = "0.0.0.0/0"
    }  
}


