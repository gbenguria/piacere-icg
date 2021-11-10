resource "aws_subnet" "aws_subnet" {
  vpc_id = aws_vpc.aws_vpc.id
  cidr_block = "{{ subnet_cidrblock }}"
  tags = {
    Name = "{{ subnetname }}"
  }

}
resource "aws_vpc" "aws_vpc" {
  cidr = "{{ vpc_cidr }}"
  tags = {
    Name = "{{ vpcname }}"
  }
}