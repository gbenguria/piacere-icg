

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
resource "openstack_compute_instance_v2" "nginx_vm" {
  name        = "nginx_host"
  image_name  = "Ubuntu-Focal-20.04-Daily-2022-04-19"
  flavor_name = "small-centos"
  key_pair    = openstack_compute_keypair_v2.ubuntu.name
  network { 
    port = openstack_networking_port_v2.i1_networking_port.id
    
  }
}

# Create floating ip
resource "openstack_networking_floatingip_v2" "nginx_vm_floating_ip" {
  pool = "external"
  # fixed_ip = ""
}

# Attach floating ip to instance
resource "openstack_compute_floatingip_associate_v2" "nginx_vm_floating_ip_association" {
  floating_ip = openstack_networking_floatingip_v2.nginx_vm_floating_ip.address
  instance_id = openstack_compute_instance_v2.nginx_vm.id
}

# Router interface configuration

resource "openstack_networking_router_interface_v2" "subnet1_router_interface" {
  router_id = openstack_networking_router_v2.router.id
  subnet_id = openstack_networking_subnet_v2.subnet1_subnet.id
}


# Attach networking port
resource "openstack_networking_port_v2" "i1_networking_port" {
  name           = "i1"
  network_id     = openstack_networking_network_v2.net1.id
  admin_state_up = true
  security_group_ids = [ openstack_compute_secgroup_v2.sg.id ]
  fixed_ip {
   subnet_id = openstack_networking_subnet_v2.subnet1_subnet.id
  }
}




## Network

# Create Network
resource "openstack_networking_network_v2" "net1" {
  name = "nginx_net"
}

# Subnet
resource "openstack_networking_subnet_v2" "subnet1_subnet" {
  name            = "subnet1_subnet"
  network_id      = openstack_networking_network_v2.net1.id
  cidr            = "16.0.0.1/24"
  dns_nameservers = ["8.8.8.8", "8.8.8.4"]
}

# Create router
resource "openstack_networking_router_v2" "router" { ## 1router, not parametric
  name                = "router"
  external_network_id = data.openstack_networking_network_v2.external.id    #External network id
}



# Create ssh keys
resource "openstack_compute_keypair_v2" "ubuntu" {
  name       = "ubuntu"
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


