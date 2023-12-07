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
#VPC
resource "aws_vpc" "{{infra_element_name}}" {
  cidr_block = "{{ addressRange }}"
  tags = {
    Name = "{{name}}"
  }
}
{##-------- Subnets Here ##}
{% for key, value in context().items() %}{% if not callable(value)%}{%if key.startswith('Subnet') %}
# Subnet
resource "aws_subnet" "{{value.name ~ "_subnet"}}" {
  vpc_id = aws_vpc.{{infra_element_name}}.id
  cidr_block = "{{ subnets | selectattr('maps', 'equalto', value.name) | map(attribute='addressRange') | first }}"
  map_public_ip_on_launch  = false
  tags = {
    Name = "{{value.name}}"
  }
}{% endif %}{% endif %}{% endfor %}
{##-------- Internet Gateway Subnets Here ##}
{% for key, value in context().items() %}{% if not callable(value)%}{%if key.startswith('InternetGateway') %}
# Internet Gateway Subnet
resource "aws_internet_gateway" "{{value.name ~ "_internet_gw_subnet"}}" {
  vpc_id = aws_vpc.{{infra_element_name}}.id
  tags = {
    Name = "{{value.name}}"
  }
}{% endif %}{% endif %}{% endfor %}

