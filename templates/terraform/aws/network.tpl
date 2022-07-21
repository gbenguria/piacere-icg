{# Copyright 2022 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#-------------------------------------------------------------------------
#}

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
