
data "aws_ami" "ami1" {
  #executable_users = ["self"]
  most_recent = true
  name_regex = "ubuntu*"
  #owners = ["self"]
  
  owners = ["099720109477"] # Canonical
}
resource "aws_instance" "instance1" {
  ami = data.aws_ami.ami1.id
  instance_type = "t2.micro"
    tags = {
     Name = "firstvm"
   }
}

data "aws_ami" "ami2" {
  #executable_users = ["self"]
  most_recent = true
  name_regex = "ubuntu*"
  #owners = ["self"]
  
  owners = ["099720109477"] # Canonical
}
resource "aws_instance" "instance2" {
  ami = data.aws_ami.ami2.id
  instance_type = "t2.micro"
    tags = {
     Name = "secondvm"
   }
}
