---
- hosts: DB
  become: yes
  vars_files:
    - vars2.yml

  pre_tasks:
  - name: Install MySQL
    apt: name={{ item }} update_cache=yes cache_valid_time=3600 state=present
    with_items:
    - mysql-server
    - mysql-client
    - python-mysqldb
    - python-setuptools
    - python-pip
    - libmysqlclient-dev

  - name: "Install Python packages"
    pip: "name={{ item }}  state=present"
    with_items:
      - PyMySQL

  - name: edit firewall
    service:
      name: ufw
      state: stopped
      enabled: false

  tasks:
  - name: Start the MySQL service
    service:
      name: mysql
      state: started
      enabled: true

  - name: update mysql password for application account
    mysql_user:
      login_unix_socket: /var/run/mysqld/mysqld.sock
      name: "{{ db_user }}"
      host: "%"
      password: "{{ db_password }}"
      state: present
      login_user: root
      login_password: test
      check_implicit_admin: yes
      priv: "*.*:ALL,GRANT"

  - name: Add the application database
    mysql_db: name="{{ db_name }}" state=present

  - name: Editing configuration file
    replace:
      path: /etc/mysql/mysql.conf.d/mysqld.cnf
      regexp: '(.*bind-addres.*)'
      replace: '#\1'

  - name: Restart MySQL
    service: name=mysql state=restarted