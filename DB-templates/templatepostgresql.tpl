resource "postgresql_database" {{ name }} {
  name              = {{ name }}
  owner             = {{ owner }}
  template          = {{ template }}
  lc_collate        = {{ lc_collate }}
  connection_limit  = {{ connection_limit }}
  allow_connections = {{ allow_connections }}
}