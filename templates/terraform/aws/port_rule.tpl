# CREATING SECURITY_GROUP
resource "aws_security_group" "{{ infra_element_name ~ "_security_group_rule" }}" { ## TOBECHANGE
  name        = "{{ infra_element_name }}"
  # description  = "Security group rule for port {{ fromPort }}"
  vpc_id      = aws_vpc.{{vpc_name}}.id ##ADD VPC NAME REFERENCE
  {% for key, value in context().items() %}{% if not callable(value)%} {%if value.kind and value.kind is defined %}
  {% if value == "INGRESS" %} ingress {% else %} egress {% endif %}  {
    from_port   = {{ value.fromPort }}
    to_port     = {{ value.toPort }}
    protocol = "{{ value.protocol }}"
    cidr_blocks = [{% for range in value.cidr %}"{{ range }}"{% endfor %}]
  }
  {% endif %}{% endif %}{% endfor %}
}