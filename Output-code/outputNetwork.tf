resource "aws_subnet" "aws_subnet" {
  vpc_id = aws_vpc.aws_vpc.id
  cidr_block = "10.0.1.0/24"
  tags = {
    Name = "Danilo"
  }

}
resource "aws_vpc" " aws_vpc " {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "Molteni"
  }
}
