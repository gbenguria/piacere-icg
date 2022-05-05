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
resource "openstack_compute_instance_v2" "nginx" {
  name        = "nginx-host"
  image_name  = "cirros"
  flavor_name = "m1.tiny"
  key_pair    = openstack_compute_keypair_v2.user_key.name
  network {
    port = openstack_networking_port_v2.nginx.id
  }
}

# Create ssh keys
resource "openstack_compute_keypair_v2" "user_key" {
  name       = "user1"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEAsRO3dcuZVB0but7Ti9eN+Ti4FvRzQfZT6DugkOnasGSwQkuBUxr0RGHYG2O+C/ul4bN4wcM8VZ4aX9bk9vwkvBkk2uJhy0ZHqIzuwzTOmRPScHWApkxGEANO4QYiYdPYdjmGgAVuKhdqPYOJc5Spkf3n4sYrU89rhC4rLyRs7doYofxpwBVaDfUExPLAtwFb2UGGzC6c0SJzqX4ZFq72NC0zs"
}

# Create floating ip
resource "openstack_networking_floatingip_v2" "nginx" {
  pool = "external"

}

# Attach floating ip to instance
resource "openstack_compute_floatingip_associate_v2" "nginx" {
  floating_ip = openstack_networking_floatingip_v2.nginx.address
  instance_id = openstack_compute_instance_v2.nginx.id
}

## Network

# Create Network
resource "openstack_networking_network_v2" "generic" {
  name = " "
}

# Create Subnet
resource "openstack_networking_subnet_v2" "nginx" {
  name            = "subnet-nginx"
  network_id      = openstack_networking_network_v2.generic.id
  cidr            = "16.0.0.0/24"
  dns_nameservers = ["8.8.8.8", "8.8.8.4"]
}

# Attach networking port
resource "openstack_networking_port_v2" "nginx" {
  name           = "nginx"
  network_id     = openstack_networking_network_v2.generic.id
  admin_state_up = true
  security_group_ids = [
    data.openstack_networking_secgroup_v2.default.id        #default flavour id
  ]
  fixed_ip {
    subnet_id = openstack_networking_subnet_v2.nginx.id
  }
}

# Router creation. UUID external gateway
resource "openstack_networking_router_v2" "generic" {
  name                = "router-generic"
  external_network_id = data.openstack_networking_network_v2.external.id    #External network id
}
# Router interface configuration
resource "openstack_networking_router_interface_v2" "nginx" {
  router_id = openstack_networking_router_v2.generic.id
  subnet_id = openstack_networking_subnet_v2.nginx.id
}

resource "openstack_compute_secgroup_v2" "http" {
  name        = "http"
  description = "Open input http port"
  rule {
    from_port   = 80
    to_port     = 80
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }
}

resource "openstack_compute_secgroup_v2" "ssh" {
  name        = "ssh"
  description = "Open input ssh port"
  rule {
    from_port   = 22
    to_port     = 22
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }
}
