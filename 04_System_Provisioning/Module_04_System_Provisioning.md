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
## Objectives
1. You get the idea of reproducible configuration as code and how it helps you scale software deployment and configuration as well.
2. By using Ansible you will learn how to maintain an well-documented version controlled configuration and handle deployment secrets like passwords and keys.
3. You can write a simple Ansible role and playbook

## Hands-on
1. Ansible training from [Galaxy Training Material](https://github.com/galaxyproject/training-material/blob/main/topics/admin/tutorials/ansible/tutorial.md)
2. Ansible playbook for a simple web app served by NGINX with MySQL database. This will demonstrate how database secrets are handled in Ansible using Ansible vault. 
### 1. Hands-on: Ansible Basics (provided by Galaxy Training Material)
**TO DO: paste and modify from GTN**

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
