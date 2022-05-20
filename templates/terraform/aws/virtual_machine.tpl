data "{{ vm }}" "ami{{ id }}" {
  #executable_users = {{ executable_users }}
  most_recent = {{ mostrecent }}
  name_regex = "{{ name_regex }}"
  #owners = {{ owners }}
  {{ filters }}
  owners = ["099720109477"] # Canonical
}
resource "aws_instance" "instance{{ id }}" {
  ami = data.aws_ami.ami{{ id }}.id
  instance_type = "{{ instance_type }}"
    tags = {
     Name = "{{ name }}"
   }
}

resource "aws_instance" "nginx-app" {
  ami = {{ os }}
  instance_type = {{ instance_type }}
  key_name = "{{ssh_key_name}}"

  network_interface {
    network_interface_id = aws_network_interface.nginx-network_interface.id
    device_index = 0
  }
}

