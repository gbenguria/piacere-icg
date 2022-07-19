# Create ssh keys
resource "openstack_compute_keypair_v2" "{{ infra_element_name }}" {
  name       = "{{ user }}"
  # public_key = "{{ user }}"
}