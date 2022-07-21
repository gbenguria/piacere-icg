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

[{{ "servers_for_" ~ name }}]
{% raw %}{{ instance_ip_{% endraw %}{{ node.vm_name }} {% raw %}}}{% endraw %}

[{{ "servers_for_" ~ name }}:vars]
ansible_connection=ssh
ansible_user={{node.vm_key_name}}
ansible_ssh_private_key_file={% raw %}{{ instance_server_private_key_{% endraw %}{{ node.vm_key_name }} {% raw %}}}{% endraw %}
