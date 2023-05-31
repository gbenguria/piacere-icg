version: '3'
services:
  {{ name }}:
    image: {{ generatedFrom.uri }}
    restart: on-failure
    ports:
    {%- for config in configs %}
    - "{{ "127.0.0.1:" ~ config.container_port }}:{{ config.iface.name }}:{{ config.vm_port }}"
    {%- endfor %}
