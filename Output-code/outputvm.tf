data "aws_ami" "ubuntu" {
  executable_users = ["self"]
  most_recent = true
  name_regex = ^myami-\d{3}
  owners = ["self"]

  filter {
   name   = "name"
   values = ["ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-*"]
  }
   filter {
   name   = "virtualization-type"
   values = ["hvm"]
  }
   
}

resource "aws_instance" "web" {

  ami = data.aws_ami.ubuntu.id
  instance_type = m6g.8xlarge

}
data "aws_ami" "ubuntu" {
  executable_users = ["self"]
  most_recent = true
  name_regex = ^myami-\d{3}
  owners = ["self"]

  filter {
   name   = "name"
   values = ["ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-*"]
  }
   filter {
   name   = "virtualization-type"
   values = ["hvm"]
  }
   
}

resource "aws_instance" "web" {

  ami = data.aws_ami.ubuntu.id
  instance_type = m6g.16xlarge

}
