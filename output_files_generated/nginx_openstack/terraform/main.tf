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
  user_name   = "admin"
  tenant_name = "test"
  password    = "wRpuXgVqBzQqGwx8Bu0sylEeb8FgjSYG"
  auth_url    = "https://127.0.0.1:5000/v3"
  insecure    = true
}
# Create virtual machine
resource "openstack_compute_instance_v2" "nginx-host" {
  name        = "nginx-host"
  image_name  = "ubuntu-20.04.3"
  flavor_name = "small"
  key_pair    = openstack_compute_keypair_v2.nginx-host_ssh_key.name
  network {
    port = openstack_networking_port_v2.ostack2.id
  }
}

# Create ssh keys
resource "openstack_compute_keypair_v2" "nginx-host_ssh_key" {
  name       = "ubuntu"
  public_key = "/home/user1/.ssh/openstack.key"
}

# Create floating ip
resource "openstack_networking_floatingip_v2" "nginx-host_floating_ip" {
  pool = "external"
  # fixed_ip = "16.0.0.1"
}

# Attach floating ip to instance
resource "openstack_compute_floatingip_associate_v2" "nginx-host_floating_ip_association" {
  floating_ip = openstack_networking_floatingip_v2.nginx-host_floating_ip.address
  instance_id = openstack_compute_instance_v2.nginx-host.id
}

