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

output "instance_server_public_key_{{ credentials }}" {
  value = openstack_compute_keypair_v2.{{ credentials }}.public_key
}

output "instance_server_private_key_{{ credentials }}" {
  value = openstack_compute_keypair_v2.{{ credentials }}.private_key
}

output "instance_ip_{{ infra_element_name }}" {
  value = openstack_compute_floatingip_associate_v2.{{ infra_element_name ~ "_floating_ip_association" }}.floating_ip
}