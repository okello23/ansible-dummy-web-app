---
Duration: 5 hours
Module: System Provisioning
Requirements:
  - shell navigation
  - linux basics
  - git basics
  - ssh configuration
Downloads required:
  - example web app repository
  - NGINX
  - MySQL
  - PostgreSQL
  - Ansible
  - Python
---
# Module 04 – System Provisioning

## Overview
In this module you will learn the basics of configuration as code. This concept helps you to keep your configuration structured, version controlled and reproducible in an event that requires redeployment.
For this particular module we use Ansible, but there are other solutions like Puppet, Salt and Werewolf.

You might ask why you need this, you might have bash scripts for installing things or simply have lists of packages and notes or small manuals how to configure them.
While this might already be a help, it will still cost you a lot of time to recover from a server loss and reproducing the exact same setup might be very difficult.  
As a motivation, you can imagine any of the following scenarios:
- You need to migrate your currently deployed software stack to a new server, but how do you make sure you don't miss anything and the new setup is configured exactly like the old one?
- A new colleague starts at your lab and asks you which software you use and how it is configured. You want to show the current state and when he or she makes their first steps, you would like to review what would be changed before the changes are applied to the live system.
- Your boss walks in and asks you to track all changes from now on, because the lab prepares for a certification process.
## Objectives
1. You get the idea of reproducible configuration as code and how it helps you scale software deployment and configuration as well.
2. By using Ansible you will learn how to maintain an well-documented version controlled configuration and handle deployment secrets like passwords and keys.
3. You can write a simple Ansible role and playbook

## Hands-on
1. Ansible training from [Galaxy Training Material](https://github.com/galaxyproject/training-material/blob/main/topics/admin/tutorials/ansible/tutorial.md)
2. Ansible playbook for a simple web app served by NGINX with MySQL database. This will demonstrate how database secrets are handled in Ansible using Ansible vault. 
### 1. Hands-on: Ansible Basics (provided by Galaxy Training Material)

> **Attribution:** This hands-on is adapted from the Galaxy Training Network (GTN) tutorial
> [Ansible Basics](https://training.galaxyproject.org/training-material/topics/admin/tutorials/ansible/tutorial.html),
> © Galaxy Training Network, licensed under the [MIT licence](https://github.com/galaxyproject/training-material/blob/main/LICENSE.md).
> Authors: Helena Rasche ([@hexylena](https://github.com/hexylena)) and Saskia Hiltemann ([@shiltemann](https://github.com/shiltemann));
> testing: Vlad Visan ([@vladvisan](https://github.com/vladvisan)).
> The content has been reformatted from GTN-specific syntax to standard Markdown.

#### Overview

In this tutorial we will briefly cover what Ansible is and how to understand what it does. This guide is not meant to make you an expert on Ansible, but perhaps give you enough that you can debug broken roles and modify them to suit your needs. Maybe even [install Galaxy using Ansible](https://training.galaxyproject.org/training-material/topics/admin/tutorials/ansible-galaxy/tutorial.html) or contribute to the [Galaxy Project's Ansible roles](https://github.com/galaxyproject?q=ansible).

This will be a very practical training with emphasis on looking at examples from modules and becoming self sufficient.

**Table of contents**

1. [What is Ansible?](#what-is-ansible)
2. [Your First Playbook and First Role](#your-first-playbook-and-first-role)
3. [Ansible Galaxy](#ansible-galaxy)
4. [Ansible Vault](#ansible-vault)
5. [Other Stuff](#other-stuff)

> **Tip: Operating system compatibility**
> These Ansible roles and training materials were last tested on Centos 7 and Ubuntu 18.04, but will probably work on other RHEL and Debian variants.
>
> The roles that are used in these training are currently used by `usegalaxy.*`, and other, servers in maintaining their infrastructure. ([US](https://github.com/galaxyproject/infrastructure-playbook/), [EU](https://github.com/usegalaxy-eu/infrastructure-playbook), both are running CentOS 7)
>
> If you have an issue running these trainings on your OS flavour, please report [the issue](https://github.com/galaxyproject/training-material/issues/new) in the training material and we can see if it is possible to solve.

#### What is Ansible?

Ansible runs commands on local or remote computers. It can move files around, create files from templates, and run command line tools. Primarily used for system administration tasks at scale. It has a push model rather than a pull model like Puppet. If you've used Puppet, Ansible doesn't evaluate what changes need to be made and make those, it just runs through all of commands every time.

Some terms that you should know first:

**Inventory file**: An Ansible-specific file that defines the systems ("hosts") and groups of hosts on which Ansible should operate.

**Ansible module**: A piece of Python code that converts some parameters into an invocation. An example would be the `command` module which converts parameters like `command: ls` into a command line that is executed. There are pre-built modules for just about everything.

**Task**: A call to an Ansible module that should be executed and the configuration for this module.

**Role**: A folder containing some tasks, templates, files, and default values for variables, with a predefined directory structure. People share roles on ["Ansible Galaxy"](https://galaxy.ansible.com/) (repository unrelated to the Galaxy Project).

**Playbook**: A YAML file listing a set of tasks and/or roles that should be applied to a group of hosts.

**Vault**: An encrypted YAML file. You put your secrets here and then you can use them in tasks, roles and playbooks.

Looking at each of these briefly:

##### Inventory file

```ini
[webservers]
192.0.2.0
192.0.2.1

[databases]
192.0.2.3 ansible_user=root
```

Here we've defined two groups of computers, `webservers` and `databases`. `ansible_user` is used to
specify which user to connect with (you need to specify that if you SSH in with a username different
than your current local user account’s name).

As you can see, in this inventory we connect to multiple remote machines. This is common practice;
Ansible playbooks are stored on your laptop or a build server, and from there Ansible connects out to the
remote machines that are managed. The advantage of running remotely is that you can manage dozens of
machines simultaneously, rather than just the local machine. This scaling out to N machines is one of
the strengths of Ansible.

Additionally, playbooks are often stored in Git or other version control repositories to ensure that
if anything happens to the infrastructure you manage, you'll still have a copy of the information
required to rebuild everything with Ansible.

<details>
<summary>Ansible Inventory Documentation (Do you connect with a different user? Password? SSH key?)</summary>

For more advanced features of the inventory file, check out [the official documentation on this topic](https://docs.ansible.com/ansible/2.9/user_guide/intro_inventory.html).

</details>

##### Roles

We can look at the [ansible-cvmfs role](https://github.com/galaxyproject/ansible-cvmfs) as an example for the layout of a role:

```
├── defaults
│   └── main.yml
├── files
│   ├── cvmfs_remount_sync.c
│   ├── cvmfs_remount_sync.centos_6
│   ├── cvmfs_remount_sync.centos_7
│   └── ...
├── handlers
│   └── main.yml
├── meta
│   └── main.yml
├── tasks
│   ├── apache.yml
│   ├── ...
│   ├── main.yml
│   └── ...
├── templates
│   ├── ...
│   └── stratum1_squid.conf.j2
└── vars
    ├── ...
    ├── main.yml
    └── ...
```

These are the folders that are included in many complex roles. Simpler roles will often not need all of the folders.

Folder    | Usage
--------- | ------
defaults  | Default values for variables the user can set (e.g. "version of software to install").
files     | These are files which should be copied as-is over to the remote location.
handlers  | This is typically used for restarting processes.
meta      | Only needed to publish your role to Ansible Galaxy (repository unrelated to the Galaxy Project).
tasks     | **Always start reading here**. This is the most important folder and the best place to start when trying to understand what an unfamiliar role does. Anything that is loaded will be referenced here (e.g. variables to load, handlers, files, templates).
templates | Files that are templated out with variables before being copied.
vars      | Default values for variables the user should normally not change (e.g. name of a package in different Linux distributions).

<details>
<summary>Ansible Role Documentation</summary>

For more information check out [the official documentation on this topic](https://docs.ansible.com/ansible/2.9/user_guide/playbooks_reuse_roles.html).

</details>

##### Modules and Tasks

A `tasks/main.yml` file calls multiple Ansible modules to accomplish its goal. A typical tasks file looks like:

```yaml
---
- name: Download cvmfs_preload utility when desired
  get_url:
    url: https://cvmrepo.web.cern.ch/cvmrepo/preload/cvmfs_preload
    dest: "{{ cvmfs_preload_path }}/cvmfs_preload"
    owner: root
    group: root
    mode: 755
  when: cvmfs_preload_install | bool

- name: Ensure AutoFS is enabled + running
  service:
    name: autofs
    enabled: yes
    state: started
```

Here we have two tasks. Each has a `name` that will be shown to the person running the playbook.

The first example invokes the [`get_url`](https://docs.ansible.com/ansible/2.9/modules/get_url_module.html) module with 5 arguments (`url`, `dest`, `owner`, `group` and `mode`). This will download a file from the location indicated in `url` to the directory specified by `dest`, change user and group ownerships to `root`, and change file permissions to `755` (as assigned by the `mode` argument). The `dest` parameter uses a [Jinja2](http://jinja.pocoo.org/) template to evaluate the value of the variable `cvmfs_preload_path`. We can [grep through](https://github.com/galaxyproject/ansible-cvmfs/search?q=cvmfs_preload_path) the repository and see that `defaults/main.yml` sets that to `/usr/bin` by default. We can override this if we need, we'll come back to that later. The first task also has a `when` condition to ensure it only runs when the `cvmfs_preload_install` variable is set.

The second invokes the [`service`](https://docs.ansible.com/ansible/2.9/modules/service_module.html) module. The arguments to this one are quite legible and the functionality can be inferred from the names for the most part: The service `name: autofs` will be `enabled` and its `state` should be `started`.

[Many modules](https://docs.ansible.com/ansible/2.9/modules/modules_by_category.html) are available for you to use.

###### Stylistic Choices

Ansible accepts two ways to format tasks:

YAML style:

```yaml
- package:
    name: "{{ package_name }}"
    state: "{{ package_state }}"
```

And an inline style.

```yaml
- package name={{ package_name }} state={{ package_state }}
```

Some groups prefer one style or another. You can mix both of these but you probably shouldn't. In the YAML style the templated value needs to be quoted if the value after the colon starts with a `{` (see [this page](https://docs.ansible.com/ansible/9/playbook_guide/playbooks_variables.html#when-to-quote-variables-a-yaml-gotcha) for more details ). The inline style does not require quoting of templated values.

##### Playbooks

```yaml
- name: CVMFS
  hosts: webservers
  vars:
    cvmfs_numfiles: 4096
  roles:
    - galaxyproject.cvmfs
```

This is a quite minimal playbook. It selects a `hosts` group named `webservers`, overrides the variable `cvmfs_numfiles`, and then says the following set of roles will be executed for this group of hosts. Ansible makes it easy to collect tasks that should apply to a group of hosts and run a playbook for all of those hosts. Some good uses of this are things like ensuring a certain set of users are installed on all of your managed machines, or using one of the package autoupdating roles to make sure your machines are up-to-date.

<details>
<summary>Ansible Playbook Documentation</summary>

For more information check out [the official documentation on this topic](https://docs.ansible.com/ansible/2.9/user_guide/playbooks_intro.html).

</details>

###### Philosophies

Different groups use playbooks differently. Here is a non-exhaustive list of ways that the author has seen playbooks used:

Strategy                                | Use Cases
--------------------------------------- | ---
A single playbook that does everything  | Works well in cloud use cases where you would rather terminate a VM and just restart from nothing. If 100% of the tasks are idempotent (can be re-run without causing problems) then this can also work well for ensuring all machines that are managed are meeting your compliance standards.
Playbooks that execute one-off commands | Works well when you have commands that cannot safely be re-run (e.g. you are managing a repository on a remote machine and executing a 'commit' action.) Also works if you have multiple people who are responsible for managing a machine but you want to ensure exactly the same commands are run each time a task needs to be done, with no variation.

##### Variables

There are a bunch of places variables can be set. [The list is ridiculous.](https://docs.ansible.com/ansible/2.9/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable) Try and find a convention within your group and stick to that to help manage the chaos.

There are some special places you can put variables that will be loaded automatically:

- `group_vars/<group_name>.yml`: if you run a playbook which has `hosts: webservers`, and `group_vars/webservers.yml` exists, it will be loaded.
- `host_vars/<host_name>.yml`: if you run a playbook and it affects host (e.g.) `api01`, and `host_vars/api01.yml` exists, it will be loaded automatically.

For a real-life example, UseGalaxy.eu [generally attempts](https://github.com/usegalaxy-eu/infrastructure-playbook) to put variables in an appropriately named `group_vars/` file.

##### Vaults

[`ansible-vault`](https://docs.ansible.com/ansible/2.9/user_guide/vault.html) is a super useful tool that lets you encrypt secrets for your group using a pre-shared key. This allows you to commit ALL of your Ansible playbooks and variables to source control, without the concern of leaking secrets. E.g. [UseGalaxy.eu](https://github.com/usegalaxy-eu/infrastructure-playbook/blob/master/secret_group_vars/all.yml)'s vault file. The encrypted version is not very interesting to look at, but it is mostly to show that we confidently place an encrypted copy of our secrets online, under configuration management. This has made our life a lot easier.


#### Your First Playbook and First Role

The above introduction was certainly not enough for you to feel confident in Ansible, so we will now build a small role and a playbook to run this role.

> **Warning: Safety First**
>
> Many of the things you can do with Ansible can be quite dangerous. As dangerous as normally being at the command line, but scaled across N machines. Be very careful with the changes you plan to make.
> Ansible provides some flags which can help you identify changes before they're made to production systems:
>
> **`--diff`**: This will show the difference whenever a file is changed.
>
> **`--check`**: Will do a dry-run of the playbook, attempting to show you which tasks will execute, which files will be updated. Not all actions can be predicted because commands are not run, if a downstream task depends on the result of a command execution task, Ansible has no way of knowing whether or not it will execute.
>
> In this tutorial we will write to files in `/tmp` as that is a *relatively* safe thing to do. The training material community does not have the resources to test this tutorial across all of the platforms you might want to run it on. Additionally we do not want to be responsible if you accidentally cause permanent damage by following this tutorial.

Requirements for Running This Tutorial:

1. You have [Ansible installed](https://docs.ansible.com/ansible/2.9/installation_guide/intro_installation.html) on the machine you will run this tutorial from

   > **Note: Running Ansible on remote machine**
   > It is possible to have Ansible installed on your laptop/local machine and run it against some remote hosts as well. We will **not** do that in this training.

2. Your `ansible` version is `>=2.7`, you can check this by running `ansible --version`

##### A Basic Role

###### Hands-on: Setting up our workspace

1. In this training we will run Ansible on the machine it will modify. This is not best practice, but it is convenient for trainings. You should probably run this in a VM either on the Cloud or in VirtualBox or similar

   All of the steps are the same, no matter which machine Ansible will manage and where you run it. The only difference is the connection setup

2. **Create a directory named `intro` and `cd` into it.**

   It's good practice to keep your deployments separated.

3. Create your inventory file (named `hosts`) in this folder

   1. We will call our group `my_hosts`

   2. Create [an inventory file](https://docs.ansible.com/ansible/2.9/user_guide/intro_inventory.html) with the group `my_hosts` and `localhost ansible_connection=local`, which tells Ansible to not use SSH, and just use the local connection. Additionally, you should explicitly set the `ansible_user` variable to the username to use when connecting to the server. Ansible has changed its behaviour over time regarding whether or not `ansible_user` is defined, and it is most effective to define it explicitly even when it can sometimes be inferred.

      <details>
      <summary>Answers</summary>

      The file should look like:

      ~~~ini
      [my_hosts]
      localhost ansible_connection=local ansible_user=ubuntu
      ~~~

      </details>
  

      <details>
      <summary>For your own infrastructure, do you connect as a different user? Password? SSH key?</summary>

      For more advanced features of the inventory file, check out [the official documentation on this topic](https://docs.ansible.com/ansible/2.9/user_guide/intro_inventory.html).

      </details>

4. Create the roles directory, your role, and the tasks folder: `mkdir -p roles/my-role/tasks/`

5. Create a YAML file in that directory, `roles/my-role/tasks/main.yml` and open it for editing

6. Define a `copy` task like below:

   ```yaml
   ---
   - name: Copy a file to the remote host
     copy:
       src: test.txt
       dest: /tmp/test.txt
   ```

   You can read about all of the parameters available to the [`copy`](http://docs.ansible.com/ansible/2.9/modules/copy_module.html) module in Ansible's documentation.

   <details>
   <summary>Ansible Module Documentation</summary>

   You can usually find a module for most commands you will run in a shell, e.g. by searching the internet for "ansible copy file to server" or "ansible restart service". If you cannot find a module that does it, there is the [`command`](http://docs.ansible.com/ansible/2.9/modules/command_module.html) module, but this should be avoided if possible. Expect to have a browser session with 10-30 different Ansible module documentation tabs if you work with Ansible regularly, no one remembers what arguments are available to every module.

   </details>

7. Create a `roles/my-role/files` folder, and within it a file named `test.txt`, containing the content "Hello, Admin 🚀"

8. This is a complete role by itself and will copy the file `test.txt` from the `roles/my-role/files/` folder over to the target host and place it in `/tmp`.

9. Create and open `playbook.yml` file for editing in the `intro` directory you created. Place the following content in there:

   ```yaml
   ---
   - hosts: my_hosts
     roles:
       - my-role
   ```

   **Question**: How does your file tree look now? Use `find` or `tree`.

   <details>
   <summary>Answers</summary>

   ```
   .
   ├── hosts
   ├── playbook.yml
   └── roles
       └── my-role
           ├── files
           │   └── test.txt
           └── tasks
               └── main.yml
   ```

   </details>

10. Run the playbook:

    **Input:**

    ```bash
    ansible-playbook -i hosts playbook.yml
    ```

    **Output:**

    ```
    PLAY [my_hosts] ****************************************************************
    TASK [Gathering Facts] *********************************************************
    ok: [localhost]
    TASK [my-role : Copy a file to the remote host] ********************************
    changed: [localhost]
    PLAY RECAP *********************************************************************
    localhost                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    ```

11. Login to the appropriate host (unless your host was `localhost`) and `cat /tmp/test.txt` to see that the change was made.

Now that you've done this, here are some starting points for exploration:

- Add more hosts, watch as Ansible executes over all of them in parallel.
- Identify a task you do regularly, e.g. restarting a service. Find the Ansible service module and add that to your playbook.

<details>
<summary> Funfact: Cowsay </summary>

> **Note: Too Many Cows?**
> If you've installed the `cowsay` tool, Ansible (for some reason) will take advantage of that to output a lot of the output with cowsay. To disable this you can `export ANSIBLE_NOCOWS=1` (Remember that exporting will only last as long as the current invocation of your terminal does, so consider adding this to your user profile if you wish to keep cowsay installed and still have legible output.)
>
> ```
>  ________________
> < PLAY [my_hosts] >
>  ----------------
>         \   ^__^
>          \  (oo)\_______
>             (__)\       )\/\
>                 ||----w |
>                 ||     ||
>  ________________________
> < TASK [Gathering Facts] >
>  ------------------------
>         \   ^__^
>          \  (oo)\_______
>             (__)\       )\/\
>                 ||----w |
>                 ||     ||
> ```

</details>

##### Facts

In the last step of the last hands-on, you ran your playbook. The first `TASK` that was executed was not one that you had written, it reads:

```
TASK [Gathering Facts] *********************************************************
ok: [localhost]
```

The [`setup`](https://docs.ansible.com/ansible/2.9/modules/setup_module.html) module runs by default for every host and gathers facts about the host.

###### Hands-on: The Setup Module

1. Run the command `ansible -i hosts -m setup my_hosts | less`.

   The `my_hosts` at the end of the command refers to the group we defined in our `hosts` inventory file.

2. Investigate the output. See what sort of information is made available to you.

   **Question**:

   1. What variable stores the OS name?
   2. Where are all of the places that you can find your machine's IP (v4) addresses?

   <details>
   <summary>Answers</summary>

   1. The OS name is stored in `ansible_distribution`. We saw `ansible_os_family` used above in the `ansible-cvmfs` role. You can use these variables if you are writing a generic role but packages or commands are named different on different operating systems.
   2. Ansible stores network information in quite a few places, sometimes one place is more convenient or more correct to use:

      - `ansible_all_ipv4_addresses`
      - `ansible_default_ipv4.address`
      - `ansible_<interface_name>.ipv4`
   </details>

##### Templates

Templates give you greater control over the files you are deploying to the target system. If you need to deploy a file to multiple hosts, but configure it differently on each host, you should use templates. For instance, deploying a service that should only listen on the correct IP address for that host would be a good use case for templates. All of the facts you discovered in the previous hands-on are available to you to use in templates, `when` statements (like the [ansible-cvmfs example we saw earlier](#modules-and-tasks)). Additionally all of the variables you've defined are available as well.

<details>
<summary>Template Syntax</summary>

Templates end with the `.j2` suffix and use Jinja2 syntax. If you are not familiar with it, you should [read about it](http://jinja.pocoo.org/docs/2.10/templates/) first, before moving on with the tutorial. Ansible fills the templates with variable values and copies the file to its remote destination without the `.j2` suffix.

</details>

###### Hands-on: Variables and Templates

1. Create the directories: `roles/my-role/templates`, `roles/my-role/defaults`

2. Create and edit a file for your role's variables, `roles/my-role/defaults/main.yml`

3. Insert the following content:

   ```yaml
   ---
   server_name: Cats!
   ```

   This will define a variable `server_name` that can then be used in templates.

4. Create and edit `roles/my-role/templates/test.ini.j2`

5. Insert the following content:

   ```ini
   [example]
   server_name = {{ server_name }}
   listen = {{ ansible_default_ipv4.address }}
   ```

6. Edit `roles/my-role/tasks/main.yml` and append a new task to the end to template this file:

   ```yaml
   - name: Template the configuration file
     template:
       src: test.ini.j2
       dest: /tmp/test.ini
   ```

7. Run the playbook again.

8. Check the contents of `/tmp/test.ini`

   **Input:**

   ```bash
   cat /tmp/test.ini
   ```

   **Output:**

   The file should look like:

   ```
   [example]
   server_name = Cats!
   listen = 192.168.0.2
   ```

   Where the last line has the machine's IP address.

   Now that this has worked successfully, we will setup a `group_vars` folder
   to show how a person using `my-role` would override the `server_name` variable.

9. Create the folder `group_vars/` (in the root of your directory)

10. Create and edit `group_vars/my_hosts.yml`

11. Insert the following:

    ```yaml
    ---
    server_name: Dogs!
    ```

    > **Tip: Variable connection**
    > When the playbook runs, as part of the setup, it collects any variables that are set. For a playbook affecting a group of hosts named `my_hosts`, it checks many different places for variables, including "group_vars/my_hosts.yml". If there are variables there, they're added to the collection of current variables. It also checks "group_vars/all.yml" (for the built-in host group `all`). There is a precedence order, but then these variables are available for roles and tasks to consume.

12. Run the playbook again, but imagine you are worried about this change, and supply the `--check --diff` flag to see what changes are made before committing to make them.

    **Input:**

    ```bash
    ansible-playbook -i hosts playbook.yml --check --diff
    ```

    > **Tip: What if you forget `--diff`?**
    > If you forget to use `--diff`, it is not easy to see what has changed. Some modules like the `copy` and `template` modules have a `backup` option. If you set this option, then it will keep a backup copy next to the destination file.
    >
    > However, most modules do not have such an option, so if you want to know what changes, always use `--diff`.

    **Output:**

    ```
    PLAY [my_hosts] ****************************************************************
    TASK [Gathering Facts] *********************************************************
    ok: [localhost]
    TASK [my-role : Copy a file to the remote host] ********************************
    ok: [localhost]
    TASK [my-role : Template the configuration file] *******************************
    --- before: /tmp/test.ini
    +++ after: /home/hxr/.ansible/tmp/ansible-local-1906887dr2u6j8n/tmptx9pdelg/test.ini.j2
    @@ -1,3 +1,3 @@
     [example]
    -server_name = Cats!
    +server_name = Dogs!
     listen = 192.168.0.25
    changed: [localhost]
    PLAY RECAP **********************************************
    localhost                  : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    ```

    Here you can see that the `server_name` value will be changed. Despite Ansible reporting `changed=1`, no changes have actually been applied to the system.

13. Run the playbook again, without the `--check` flag to apply your changes.

> **Note: Ansible Variable Templating**
> In this hands-on we used some templated variables. We defined them in a template, but they are also commonly used in the group variables file. Our templated variable looked like: `listen = {{ ansible_default_ipv4.address }}`.
>
> It is common to see things like this in Ansible roles:
>
> ```yaml
> root_dir = /opt/my-app
> config_dir = "{{ root_dir }}/config"
> ```
>
> When Ansible runs:
>
> 1. It collects variables defined in group variables and other places
> 2. The first task for each machine is the [`setup` module](https://docs.ansible.com/ansible/2.9/modules/setup_module.html) which gathers facts about the host, which are added to the available variables
> 3. When multiple roles execute in a playbook:
>    1. Their defaults are added to the set of variables (the group variables having precedence over these variables)
>    2. They can also dynamically define more variables which may not be set until that role is run
> 4. Before use (in templates, commands, etc.), variables are resolved to their final value


#### Ansible Galaxy

Now that you've built a small role, you can imagine that building real roles that manage the full installation of a piece of software are not simple things. Ansible Galaxy (repository unrelated to the Galaxy Project) is the answer here. Many roles for common administration tasks, and software installation and setup are readily available on Ansible Galaxy.

**Warning**: This will install Memcached on the target machine.

###### Hands-on: Installing a module using ansible-galaxy

1. Install the geerlingguy.memcached role with ansible-galaxy into your roles folder:

   **Input:**

   ```bash
   ansible-galaxy install \
       -p roles/ geerlingguy.memcached
   ```

   **Output:**

   This will install the new role into your `roles` folder, alongside your own role.

   ```
   - downloading role 'memcached', owned by geerlingguy
   - downloading role from https://github.com/geerlingguy/ansible-role-memcached/archive/1.1.0.tar.gz
   - extracting geerlingguy.memcached to /home/ubuntu/ansible/intro/roles/geerlingguy.memcached
   - geerlingguy.memcached (1.1.0) was installed successfully
   ```

2. Edit your playbook.yml and add the role `geerlingguy.memcached` at the bottom, after `my-role`

3. Run the playbook

   **Question**: Did something go wrong?
   <details>
   <summary>Answers</summary>

   Since you have been running the playbook as a non-root user (or at least you should have been!), the step to install a package fails.
   The solution to this is to set `become: true`.

   1. Edit your playbook.yml
      - add `become: true` just below `hosts: my_hosts`
   2. Run the playbook again

   `become` causes Ansible to attempt to become a different user (using sudo/su/whatever is appropriate), by default this is `root`. If you want to become a different user, just set `become_user`. Beware, the user should be able to privilege escalate without a password prompt. Otherwise when you execute the playbook you should set `--ask-become-pass`, using the privilege escalation password for that host.
   </details>

</br>

   <details>
   <summary>Excursion: Ansible Become</summary>

   See the [documentation](https://docs.ansible.com/ansible/2.9/user_guide/become.html) if you need to control this behaviour differently. `become` can be set either at the task level or the playbook level.

   </details>

</br>

   > **Tip: Should I use sudo or directly login as root?**
   > This is often site-specific policy. If your site doesn't have a dictated policy, then it's generally preferable to not allow direct login as root, and login as a separate user.

##### Choosing a Role

Picking the best role for a task from Ansible Galaxy is not always a trivial task. Sometimes there will only be a single role doing what you need. Other times you'll have to choose between 20 different roles that all look more or less the same. Here are some tips to guide you in identifying appropriate and well-written roles:

- The name should match the software you are using (I.e. ignore a role named `stackstorm` when you are trying to set up `rabbitmq`. Ansible Galaxy does not have perfect search.)
- `geerlingguy` wrote a huge number of roles for many pieces of standard software. If there is a role from this person, this is usually a safe choice. In the same way we recommend `galaxyproject` and `usegalaxy_eu` roles.
- Check the GitHub readme of each role you consider using. Look for:
  - Extensive documentation of all of the variables, their default values, and how they behave.
  - An example playbook using the role
- A large number of downloads is a good sign that other people found it useful

These are usually good proxies for quality, but do not treat them as strict rules. For an example of a role meeting many of these qualities, [`ansible-cvmfs`](https://github.com/galaxyproject/ansible-cvmfs) is good; the variables are well documented and there are example playbooks that you can (more or less) copy-and-paste and run.

Sometimes a role will accomplish 95% of what you need to do, but not everything. Once you have installed the role with `ansible-galaxy install`, you can edit it locally to make any changes. In an ideal world you would contribute this back, but this is not always a high priority. Many projects copy roles directly into their repositories, e.g. [galaxyproject](https://github.com/galaxyproject/infrastructure-playbook/tree/master/roles) and [usegalaxy.eu](https://github.com/usegalaxy-eu/infrastructure-playbook/tree/master/roles)

> **Tip: How do I know what I can do with a role? What variables are available?**
> You don't. There is no standard way for reporting this, but well written roles by trusted authors (e.g. geerlingguy, galaxyproject) do it properly and write all of the variables in the README file of the repository. We try to pick sensible roles for you in this course, but, in real life it may not be that simple.
>
> So, definitely check there first, but if they aren't there, then you'll need to read through `defaults/` and `tasks/` and `templates/` to figure out what the role does and how you can control and modify it to accomplish your goals.

#### Ansible Vault

Now that you have a small role built up, you might start thinking about deploying larger and more complex services and infrastructure. One last common task we want to cover here is the inclusion of secrets. Ansible Vault is really useful to include encrypted secrets in your playbook repository.

###### Hands-on: Setting up secrets

1. Run `mkdir -p secret_group_vars`

2. Now we'll create a strong password: `openssl rand -base64 24 > vault-password.txt`

3. Run `ansible-vault create secret_group_vars/all.yml --vault-password-file=vault-password.txt`

   This will open `secret_group_vars/all.yml` in your text editor.

4. In this file, enter the following contents and save it:

   ```yaml
   apikey: super-secret-api-key-wow!
   ```

   **Question**: How does your file look? Is it readable? Run `cat secret_group_vars/all.yml`

   <details>
   <summary>Answers</summary>

   The file will look like this, it is encrypted by Ansible Vault with AES256 encryption.

   ```
   $ cat secret_group_vars/all.yml
   $ANSIBLE_VAULT;1.1;AES256
   64373665366130333437393639343534653134346538636239393363373062393830653333323966
   3134333366363130326139323162323131643763336236320a393262303938316262643764323862
   36393161666663353231366336613838633866323230303031313465646333613862363264323139
   3263383530626262370a666139666462663938343531656432353239346532316630366165376566
   34313765353766666330366632303836353863396430343264303032363739666139383830323565
   6133663637356331613062353834646561653366386665623930
   ```

   </details>

5. Use the new variable in our `.ini` file from earlier. Edit `roles/my-role/templates/test.ini.j2` and add the line `apikey = {{ apikey }}`

6. Add encrypted variable file to `playbook.yml`

   ```yaml
   - hosts: my_hosts
     ...
     vars_files:
      - secret_group_vars/all.yml
   ```

7. Tell ansible where to find the decryption file. Create file `ansible.cfg` with content

   ```yaml
   [defaults]
   vault_password_file=vault-password.txt
   ```

8. Run the playbook

9. Check the contents of `/tmp/test.ini`

   **Input:**

   ```bash
   cat /tmp/test.ini
   ```

   **Output:**

   The file should look like:

   ```ini
   [example]
   server_name = Dogs!
   listen = 192.168.0.2
   apikey = super-secret-api-key-wow!
   ```

In real life scenarios where you are sharing your playbooks publicly, be sure to encrypt all secrets from the start (or remove any secrets from the git history if you ever committed them in plain text). If you are storing your vault password in a file, remember to add it to your `.gitignore` (or VCS appropriate file.)

#### Other Stuff

Ansible has a huge array of features and we can't cover them all. Some commonly used features are documented below:

##### With Items

Duplicating tasks ten times to install ten packages is not efficient, so Ansible provides `loop` construct

```yaml
- name: Install stuff
  package:
    name: "{{ item }}"
    state: installed
  loop:
    - htop
    - git
    - vim
```

This works for any task, not just package installation, if you have things you'd like to repeat.
Note that for this task one would normally list multiple packages in the `name` parameter of the package module.

```yaml
- name: Install stuff
  package:
    name:
      - htop
      - git
      - vim
    state: installed
```

##### When Changed

Doing something only when a task is in the "changed" state is a common pattern. This is often used for reloading a service when some configuration files have changed.

```yaml
- name: Copy configuration file
  copy:
    src: main.conf
    dest: /etc/service/main.conf
    owner: root
    group: root
    mode: 0644
  register: service_conf

- name: Restart the service
  service:
    name: service
    enabled: yes
    state: restarted
  when: service_conf is changed
```

##### Notifying Handlers

Often you want to restart a service whenever something has changed, like above. But if you need to restart the service whenever one of many different tasks has changed, there is a simpler way than writing `when: a.changed or b.changed or c.changed or ...`

First, move the restarting or reloading of the service into the `handlers/main.yml`

```yaml
- name: restart service
  service:
    name: service
    enabled: yes
    state: restarted

- name: reload httpd
  service:
    name: httpd
    enabled: yes
    state: reloaded
```

Now you can change your task definitions:

```yaml
- name: Copy configuration file
  copy:
    src: main.conf
    dest: /etc/service/main.conf
    owner: "root"
    group: "root"
    mode: "0644"
  notify: 'restart service'
```

We no longer `register` the command, instead the `notify` attribute automatically marks that the appropriate handler should be called *at the end of the playbook run*. Additionally, tasks from outside of this role can use the same `notify`. So if you use a community built role for managing apache, and then have a custom role that builds the apache configuration, you can use changes there to reload the service using their definition of the reload/restart.

### 2. Hands-on: Deploy a simple web app using a ready-made playbook
-> Lives on a dedicated GitHub repositoring (Code+Ansible)
**TO ADD**

1. Clone the repo
2. Configure your Ansible inventory (based on the provided setup)
3. Run the deployment
4. Test the app
## Quizzes
1. Write a simple role
2. Write a playbook that applies your role to a set of hosts
3. Adapt the provided playbook and customize the web app using variables and Ansible vault. Change the HTML template, the DB password and change the database used (advanced). Use git as SCM so you can switch back and forth between changes.

### 1. Quiz: Write a simple ansible role
It should use at least one variable, and consist of `tasks/main.yml` and `defaults/main.yml`
### 2. Quiz: Write a playbook that uses your role.
1. Can you use host vars to configure the role depending on the target host?
2. *Bonus:* Can you extend the role to use a handler?
### 3. Quiz: Can you use Ansible to customize the web app? 
1. Change the name and the logo!
2. Now set a secure password for your database.
3. Switch the database from MySQL to PostgreSQL.
