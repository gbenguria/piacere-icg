---
- hosts: {{ "servers_for_" ~ name }}
  gather_facts: no
  become: yes
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
        dest: {% raw %}"{{ item }}"{%endraw%}
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
        - {{ source_code }}

