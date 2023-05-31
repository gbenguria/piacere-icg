resource "aws_launch_template" "{{infra_element_name}}" {
  name_prefix   = "{{name}}_"
  //image_id      = "ami-1a2b3c"
  {%- for key, value in context().items() %}{% if not callable(value)%}{%if key.lower().startswith('virtualmachine') %}
  instance_type = "{{value.sizeDescription}}"
  image_id      = "{{value.os}}"
  {%- endif %}{% endif %}{% endfor %} 
}

resource "aws_autoscaling_group" "{{infra_element_name}}" {
  desired_capacity   = {{min}}
  max_size           = {{max}}
  min_size           = {{min}}

  launch_template {
    id      = aws_launch_template.{{infra_element_name}}.id
    version = "$Latest"
  }
}