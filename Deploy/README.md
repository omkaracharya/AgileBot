## DEPLOYMENT
 
#### Note: For running acceptance tests on your own deployed version, make sure that your environment has access tokens to Rally Project, Slack Room and GitHub. Instruction on how to set them is provided further down this file.
 
To deploy your version of AgileBot, follow the below mentioned steps. 

1. Install the vagrant to create the virtual machine. Follow [these](https://github.com/CSC-DevOps/CM/blob/master/VM.md) instructions.  

    **Note:** If you already have host machine directly jump to step 4.  

2. Reserve a virtual machine with CentOS/Ubuntu base image and login.
   a. Initialize virtual machine

   ```
   vagrant init centos/7   
   ```
   b. Start the vm

   ```
   vagrant up
   ```

3. Get the ssh configuration. 

    ```
   vagrant ssh-config
    ```

4. Clone this repo and update the inventory file.

   a. provide the correct IP address of the virtual machine. 
   
   b. update the `ansible_ssh_user` name. 
   
   c. update the `ansible_ssh_private_key_file` path.
   
   ##### *Hint: Copy the IdentityFile path from vagrant ssh-config path. If you are not using vagrant then provide private key file path.*

5. Install ansible. 

    ```
    yum install ansible
    ```

6. Test reachability of the virtual machine using inventory file.

    ```
    ansible all -m ping -i inventory 
    ```

7. Update the environment variables in the environment file `ansible/env.conf` according to you target systems.

      ```
      AGILEBOT_ID=
      AGILEBOT_TOKEN=
      SLACK_TOKEN=
      RALLY_SERVER=rally1.rallydev.com
      RALLY_USERNAME=
      RALLY_PASSWORD=
      RALLY_APIKEY=
      RALLY_PROJECT=AgileBot
      CHROME_DRIVER_PATH=
      SLACK_URL=https://csc510project.slack.com/
      TESTER_EMAIL=
      TESTER_PASSWORD=
      MOCK=False
      GITHUB_TOKEN=
      FLASK_PORT=4500
      REPO_NAME=
      REPO_AUTHOR=
      ```

    ##### *Note: While running, we pass this environment file as input file to docker in ansible-playbook. AgileBot uses these environment variables throughout its lifespan*

8. Run the ansible playbook 

    ```
    ansible-playbook -i inventory ansible/ansible.yaml
    ```

9. [Slack side configuration] Configure the public IP address of Virtual Machine in slack for interactive messages. 

   a. Open this url https://api.slack.com/apps/A7N5G20GY/interactive-messages. 

   b. Update the public IP address in the Request URL.

      For ex: if Public IP address of VM is `152.7.99.153` then Request URL should be http://152.7.99.153:4500/slack/message_actions. 

   ##### *Note: No need to change the port number*.

   c. Save the changes.

