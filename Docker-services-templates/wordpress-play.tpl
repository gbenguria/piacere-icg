---
- hosts: APP1
  become: yes

  vars_files:
    - wordpress-vars.yml

  pre_tasks:
    - name: "Install packages"
      ###OS###: "name={{ item }} state=present"
      with_items:
###OS_PACKETS###

    - name: "Install Python packages"
      pip: "name={{ item }}  state=present"
      with_items:
        - docker

  tasks:
    - name: Start a WP container
      community.docker.docker_container:
        name: wordpress
        image: wordpress:5.8.0
        state: started
        env:
          WORDPRESS_DB_HOST: "{{WORDPRESS_DB_HOST}}"
          WORDPRESS_DB_USER: "{{WORDPRESS_DB_USER}}"
          WORDPRESS_DB_PASSWORD: "{{WORDPRESS_DB_PASSWORD}}"
          WORDPRESS_DB_NAME: "{{WORDPRESS_DB_NAME}}"
          WORDPRESS_TABLE_PREFIX: "{{WORDPRESS_TABLE_PREFIX}}"
        ports:
          - "8080:80"
        volumes_from:
          - mydata