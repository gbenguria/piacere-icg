resource "openstack_compute_secgroup_v2" "{{ name }}" {
  name        = "{{ name }}"
  description  = "Security group rule for port {{ from_port }}-{{ to_port }}"
  rule {
    from_port   = {{ fromPort }}
    to_port     = {{ toPort }}
    ip_protocol = "{{ protocol }}"
    cidr        = [
        {% for range in addressRanges %}
        {{ range }},
        {% endfor %}
    ]
  }
}