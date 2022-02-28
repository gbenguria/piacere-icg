---
- hosts: {{ address }}
  gather_facts: no
  become: yes
  vars:
    ansible_ssh_private_key_file: "{{ ssh_key_file }}"
    ansible_ssh_user: "{{ ssh_user }}"
  tasks:
    - name: Update repositories
      apt:
        update_cache: yes

    - name: Install nginx
      package:
        name: nginx

    - name: Start nginx
      service:
        name: nginx
        enabled: yes
        state: started

    - name: Set attributes
      set_stats:
        data:
          site_config_dir: /etc/nginx/conf.d

    - name: Install sample site
      copy:
        dest: "{{ item }}"
        content: |
          <!doctype html>
          <html lang="en">
          <head>
            <title>Hello World!</title>
          </head>
          <body>
            <h1>Sample web page</h1>
            <p>With little content ;)</p>
          </body>
          </html>
      with_items:
        - /var/www/html/index.html
        - /usr/share/nginx/html/index.html

