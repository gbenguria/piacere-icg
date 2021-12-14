yum update
yum install epel-release
yum install ansible
## create the known_hosts
ansible-galaxy collection install community.docker

## maybe run 2 times the same playbook if the symbolic link creation fails