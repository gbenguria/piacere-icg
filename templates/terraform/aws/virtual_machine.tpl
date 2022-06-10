resource "aws_instance" "{{name}}" {
  ami = "{{ os }}"
  instance_type = "{{ instance_type }}"
  key_name = "{{ssh_key_name}}"

  network_interface {
    network_interface_id = aws_network_interface.{{i1.belongsTo ~ "_network_interface"}}.id
    device_index = 0
  }
}
