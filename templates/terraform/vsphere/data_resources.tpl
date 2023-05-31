data "{{type}}" "{{name}}" {
  name          = "{{gname}}"
{%- for key, value in context().items() %}{% if value is mapping%}{% if value.type == "vsphere_datacenter"%}
  datacenter_id = ${data.vsphere_datacenter.{{value.name}}.id} 
{% endif %}{% endif %}{% endfor %}
}
