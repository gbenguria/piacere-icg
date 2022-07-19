[{{ "servers_for_" ~ name }}]
{% raw %}{{ instance_ip_{% endraw %}{{ node.vm_name }} {% raw %}}}{% endraw %}

[{{ "servers_for_" ~ name }}:vars]
ansible_connection=ssh
ansible_user={{node.vm_key_name}}
ansible_ssh_private_key_file={% raw %}{{ instance_server_private_key_{% endraw %}{{ node.vm_key_name }} {% raw %}}}{% endraw %}
