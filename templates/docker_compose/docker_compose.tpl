version: '3'
services:
  {{ name }}:
    image: {{ generatedFrom.uri }}
    restart: on-failure
    {%- for image in extra_parameters %}{% if image["maps"] is sameas generatedFrom["name"] %}{% for cont in image["generatedContainers"] %}{% if cont["name"] is sameas name %}{% if "hostConfigs" in cont %}
    ports:
    {%- for config in cont["hostConfigs"][0]["configurations"] %}
    - "{{ config.container_port }}:{{ config.vm_port }}"
    {%- endfor %}
    {%- if cont["hostConfigs"][0]["environment_variables"] is defined %}
    environment:
    {%- for environ in cont["hostConfigs"][0]["environment_variables"] %}
      {{ environ.key }}: "{{ environ.value }}"
    {%- endfor %}{% endif %}
    {%- endif %}{% endif %}{% endfor %}{% endif %}{%- endfor %}
{%- if networks is defined %}
    networks:
      - {{ networks.0.name }}

networks:
  {{ networks.0.name }}:
    name: {{ networks.0.containerNetworkName }}
{%- endif %}