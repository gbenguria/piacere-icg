# CREATING SECURITY_GROUP
{% for key, value in context().items() %}{% if not callable(value)%} {%if value.kind and value.kind is defined %}
resource "openstack_compute_secgroup_v2" "{{ key }}" {
  name        = "{{ key }}"
  description  = "Security group rule for port {{ value.fromPort }}"
  rule {
    from_port   = {{ value.fromPort }}
    to_port     = {{ value.toPort }}
    ip_protocol = "{{ value.protocol }}"
    cidr        = {% for range in value.cidr %}"{{ range }}"{% endfor %}
  }
}
{% endif %}{% endif %}{% endfor %}