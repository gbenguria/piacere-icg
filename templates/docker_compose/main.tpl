---
- hosts: {{ "servers_for_" ~ name }}
  gather_facts: no
  become: yes
  tasks:
    - name: Copy over docker compose
      copy:
        src: docker_compose.yml
        dest: .
    - name: Deploy application
      docker_compose:
        definition: docker_compose.yml
