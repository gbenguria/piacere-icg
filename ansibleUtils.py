from ansibleBuilder import *

def generic_matcher(template_list, specific_data):
    matching_lines = [s for s in template_list if "###" in s]
    for line in matching_lines:
        line_plit = line.split('###')
        var = line_plit[1]
        index = template_list.index(line)
        template_list[index] = line_plit[0]+specific_data[var]+line_plit[2]
    return template_list

def databases_postgres(template_list, template_data, kind):
    if kind == "vars":
        new_template_list = generic_matcher(template_list, template_data[kind])
    if kind == "play":
        if template_data[kind]["OS"] == "debian":
            specific_data = {"OS": "apt", "OS_PACKETS": "        - postgresql-10"}
        elif template_data[kind]["OS"] == "centos":
            specific_data = {"OS": "yum", "OS_PACKETS": "        - postgresql10\n        - postgresql10-server\n        - postgresql10-contrib\n        - postgresql10-libs"}
        new_template_list = generic_matcher(template_list, specific_data)
    return "".join(new_template_list)

def databases_mysql(template_list, template_data, kind):
    if kind == "vars":
        new_template_list = generic_matcher(template_list, template_data[kind])
    if kind == "play":
        if template_data[kind]["OS"] == "debian":
            specific_data = {"OS": "apt", "OS_PACKETS": "    - mysql-server\n    - mysql-client\n    - python-setuptools\n    - python-mysqldb\n    - libmysqlclient-dev\n    - python3-pip"}
        elif template_data[kind]["OS"] == "centos":
            specific_data = {"OS": "yum", "OS_PACKETS": "        - postgresql10\n        - postgresql10-server\n        - postgresql10-contrib\n        - postgresql10-libs"}
        new_template_list = generic_matcher(template_list, specific_data)
    return "".join(new_template_list)

def service_wordpress(template_list, template_data, kind):
    if kind == "vars":
        new_template_list = generic_matcher(template_list, template_data[kind])
    if kind == "play":
        if template_data[kind]["OS"] == "debian":
            specific_data = {"OS": "apt", "OS_PACKETS": "        - python3\n        - python3-pip\n        - docker\n        - docker.io"}
        elif template_data[kind]["OS"] == "centos":
            specific_data = {"OS": "yum", "OS_PACKETS": "        - docker"}
        new_template_list = generic_matcher(template_list, specific_data)
    return "".join(new_template_list)