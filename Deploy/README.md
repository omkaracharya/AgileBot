### Deployment Steps

To run the agile bot, please follow the below mentioned steps. 

1. Install the vagrant to create the virtual machine. (follow these instructions [install](https://github.com/CSC-DevOps/CM/blob/master/VM.md)).  

    **Note:** If you already have host machine then please directly jump to step 4.  

2. Please reserve a virtual machine with ubuntu base image. 

```
a. initialize virtual machine

    vagrant init centos/7

b. start the vm

    vagrant up
```

3. Get the ssh configuration. 

```
   vagrant ssh-config
```

4. Update the inventory file.

```
   a. provide the correct IP address of the virtual machine. 
   
   b. update the `ansible_ssh_user` name. 
   
   c. update the `ansible_ssh_private_key_file` path.
   
   Hint: Copy the IdentityFile path from vagrant ssh-config path. If you are not using vagrant then please provide private key file path. 
```   

5. Install ansible. 

```
   yum install ansible
```

6. Test reachability of the vitrual machine using inventory file.

```
   ansible all -m ping -i inventory 
```

6. Run the anisble playbook 

```
   ansible-playbook -i inventory ansible/ansible.yaml
```
