

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


# Create virtual machine
resource "openstack_compute_instance_v2" "vm1" {
  name        = "nginx-host"
  image_name  = "Ubuntu-Focal-20.04-Daily-2022-04-19"
  flavor_name = "small"
  key_pair    = openstack_compute_keypair_v2.user1.name
  network {
    port = openstack_networking_port_v2.net1.id
  }
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
  name = "concrete_net"
}

# Create Subnet
resource "openstack_networking_subnet_v2" "net1_subnet" {
  name            = "concrete_net_subnet"
  network_id      = openstack_networking_network_v2.net1.id
  cidr            = "16.0.0.0/24"
  dns_nameservers = ["8.8.8.8", "8.8.8.4"]
}

# Attach networking port
resource "openstack_networking_port_v2" "net1" {
  name           = "concrete_net"
  network_id     = openstack_networking_network_v2.net1.id
  admin_state_up = true
  security_group_ids = [
  openstack_compute_secgroup_v2.icmp.id,
  openstack_compute_secgroup_v2.http.id,
  openstack_compute_secgroup_v2.https.id,
  openstack_compute_secgroup_v2.ssh.id,
  
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



# CREATING SECURITY_GROUP
  
resource "openstack_compute_secgroup_v2" "icmp" {
  name        = "icmp"
  description  = "Security group rule for port -1"
  rule {
    from_port   = -1
    to_port     = -1
    ip_protocol = "icmp"
    cidr        = "0.0.0.0/0"
  }
}
 
resource "openstack_compute_secgroup_v2" "http" {
  name        = "http"
  description  = "Security group rule for port 80"
  rule {
    from_port   = 80
    to_port     = 80
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }
}
 
resource "openstack_compute_secgroup_v2" "https" {
  name        = "https"
  description  = "Security group rule for port 443"
  rule {
    from_port   = 443
    to_port     = 443
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }
}
 
resource "openstack_compute_secgroup_v2" "ssh" {
  name        = "ssh"
  description  = "Security group rule for port 22"
  rule {
    from_port   = 22
    to_port     = 22
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }
}




# Create ssh keys
resource "openstack_compute_keypair_v2" "user1" {
  name       = "user1"
  # public_key = "user1"
}

