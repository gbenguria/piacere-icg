---
- hosts: DB
  become: yes

  pre_tasks:
    - name: "Install packages"
      apt: "name={{ item }} state=present"
      with_items:
        - postgresql-10
        - python3
        - python3-pip

    - name: "Install Python packages"
      pip: "name={{ item }}  state=present"
      with_items:
        - psycopg2-binary

  tasks:
 
    - name: "Start and enable services"
      service: "name={{ item }} state=started enabled=yes"
      with_items:
        - postgresql

    - name: "Create app database"
      postgresql_db:
        state: present
        name: "{{ db_name }}"
      become: yes
      become_user: postgres

    - name: "Create db user"
      postgresql_user:
        state: present
        name: "{{ db_user }}"
        password: "{{ db_password }}"
      become: yes
      become_user: postgres

    - name: "Grant db user access to app db"
      postgresql_privs:
        type: database
        database: "{{ db_name }}"
        roles: "{{ db_user }}"
        grant_option: no
        privs: all
      become: yes
      become_user: postgres

    - name: "Allow md5 connection for the db user"
      postgresql_pg_hba:
        dest: "/etc/postgresql/10/main/pg_hba.conf"
        contype: host
        databases: all
        method: md5
        users: "{{ db_user }}"
        create: true
      become: yes
      become_user: postgres
      notify: restart postgresql