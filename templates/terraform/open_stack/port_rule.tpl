resource "openstack_compute_secgroup_v2" "{{ name ~ "_secgroup" }}" {
  name        = "{{ name }}"
  description  = "Security group rule for port {{ from_port }}-{{ to_port }}"
  rule {
    from_port   = {{ from_port }}
    to_port     = {{ to_port }}
    ip_protocol = "{{ ip_protocol }}"
    cidr        = "{{ ipv6_cidr_blocks }}"
  }
}