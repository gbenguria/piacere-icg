resource "aws_subnet" "aws_subnet" {
  vpc_id = aws_vpc.aws_vpc.id
  cidr_block = "10.0.1.0/24"
  tags = {
    Name = "piacere_subnet"
  }

}
resource "aws_vpc" "aws_vpc" {
  cidr = "10.0.0.0/16"
  tags = {
    Name = "piacere_vpc"
  }
}
