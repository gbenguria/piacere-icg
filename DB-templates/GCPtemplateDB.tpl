resource "google_sql_database" "database" {
  name     = "{{ name }}"
  instance = {{ instance }}
}

resource "google_sql_database_instance" "instance" {
  name   = "{{ instance_name }}"
  region = "{{ region }}"
  settings {
    tier = "{{ tier }}"
  }

  deletion_protection  = "{{ deletion_protection }}"
}