resource "google_compute_instance" "{{ default }}" {
  name         = "{{ name }}"
  machine_type = "{{ machine_type }}"
  zone         = "{{ zone }}"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  scratch_disk {
    interface = "SCSI"
  }

  network_interface {
    network = "default"

    access_config {
    }
  }

}