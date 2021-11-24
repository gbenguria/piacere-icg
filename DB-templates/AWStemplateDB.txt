resource "aws_db_instance" "{{ identifier }}" {
  identifier             = "{{ identifier }}"
  instance_class         = "{{ instance }}"
  allocated_storage      = {{ storage }}
  engine                 = "{{ engine }}"
  engine_version         = "{{ version }}"
  username               = "{{ username }}"
  password               = {{ password }}
  db_subnet_group_name   = {{ subnet }}
  vpc_security_group_ids = {{ security }}
  parameter_group_name   = {{ parameter }}
  publicly_accessible    = {{ accessible }}
  skip_final_snapshot    = {{ skip }}
}