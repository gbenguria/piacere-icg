{%- for config in configs %}
{%- raw %}{{ instance_server_private_key_{% endraw %}{{ config.host.credentials }}{% raw %}_{%- endraw %}{{config.host.name}}{% raw %} }}
{% endraw %}
{%- endfor %}
