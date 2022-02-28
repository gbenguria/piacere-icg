---
- hosts: APP1
  become: yes

  pre_tasks:
    - name: "Install packages"
      apt: "name={{ item }} state=present"
      with_items:
        - docker

    - name: Remove a symbolic link
      ansible.builtin.file: 
        path: /usr/bin/python
        state: absent

    - name: Create a symbolic link
      ansible.builtin.file: 
        src: /usr/bin/python3
        dest: /usr/bin/python
        state: link
      register: result
      retries: 3
      delay: 5
      until: result is not failed

    - name: Create a symbolic link
      ansible.builtin.file: 
        src: /usr/bin/pip3
        dest: /usr/bin/pip
        state: link
      register: result
      retries: 3
      delay: 5
      until: result is not failed
    
    - name: "Install Python packages"
      pip: "name={{ item }}  state=present"
      with_items:
        - docker

    - name: edit firewall
      service:
        name: ufw
        state: stopped
        enabled: false
        
  tasks:
    - name: Create a volume
      community.docker.docker_volume:
        name: mydata
        
    - name: Start a WP container
      community.docker.docker_container:
        name: wordpress
        image: wordpress:5.8.0
        state: started
        env:
          WORDPRESS_DB_HOST: "{{ wordpress_db_host }}"
          WORDPRESS_DB_USER: "{{ wordpress_db_user }}"
          WORDPRESS_DB_PASSWORD: "{{ wordpress_db_password }}"
          WORDPRESS_DB_NAME: "{{ wordpress_db_name }}"
          WORDPRESS_TABLE_PREFIX: "{{ wordpress_table_prefix }}"
        ports:
          - "8080:80"
        volumes:
          - mydata