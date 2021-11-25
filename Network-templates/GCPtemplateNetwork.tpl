resource "google_compute_network" "vpc_network" {
name = "{{ network }}"
}
resource "google_compute_subnetwork" "public-subnetwork" {
name = "{{ subnetwork }}"
ip_cidr_range = "10.2.0.0/16"
region = "us-central1"
network = google_compute_network.vpc_network.name
}
