---
engine: terraform
input:
  - OS_USERNAME
  - OS_PASSWORD
  - OS_AUTH_URL
  - OS_PROJECT_NAME
output:
{% for vm in vms %}
  - instance_server_public_key_{{ vm.vm_key_name }}
  - instance_server_private_key_{{ vm.vm_key_name }}
  - instance_ip_{{ vm.vm_name }}
{% endfor %}
...
