resource "aws_vpc" "{{infra_element_name}}" {
  cidr_block = "{{ addressRange }}"
  tags = {
    Name = "{{name}}"
  }
}

resource "aws_subnet" "{{infra_element_name ~ "_subnet"}}" {
  vpc_id = aws_vpc.{{infra_element_name}}.id
  cidr_block = "{{vpc_subnet.addressRange}}"
  # map_public_ip_on_launch = true
  tags = {
    Name = "{{name}}"
  }
}

resource "aws_network_interface" {{infra_element_name ~ "_network_interface"}} {
  subnet_id = aws_subnet.{{infra_element_name ~ "_subnet"}}.id
  security_groups = [aws_security_group.{{ name ~ "_security_group_rule" }}.id] ##TOBECHANGED
  tags = {
    Name = "{{infra_element_name ~ "_network_interface"}}"
  }
}
