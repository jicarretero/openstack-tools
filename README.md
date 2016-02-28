# openstack-tools
Some easy tools to interact or do things with openstack.

## simple_token.py
----------------
Once set the variables "OS_USERNAME", "OS_PASSWORD" and "OS_AUTH_URL" it gets one token for each Tenant. The response is given in 
pairs:
<tenant> <token>

    usage: simple_token.py

This script uses http requests. It is known to work in Juno version

## backup_os
----------
This is a bash script to "backup" mysql databases and configuration files. 
    
    usage: backup_os

There are a few vars at the beginning of the script which might be useful to change:

The backup directory, where the configuration/database files are stored is:

    BACKUP_DIR=.... 

The files where mysql connect information is retrieved from is:

    backups=(
       '/etc/keystone/keystone.conf'
       .....
    )

The configuration directories to be saved are:

    backup_configs=(
        '/etc/keystone'
        ...
    )

This is the really first version of the script and it only includes mysql databases.

### Known Issues:
* The regular expression to extract the database parameters is quite simple, and needs to be heavily improved in order to be able to access more databases.

## openstack-config
------------------
Nice tool to configure openstack by RedHat. I needed --get parameter, so I added it.

## vview
--------
It uses virt-viewer to show the console of any VM in an openstack. You have to set the system variables OS_USERNAME, OS_PASSWORD, etc. from the administrator. and you could use:

   vview <uuid|id>

You need to be able to resolve the compute nodes either using DNS or using /etc/hosts and ssh connection in order to use this tool.

### Known limitations
* You need to have the "admin" credentials for Openstack.
* It is only known to work in Linux systems since virt-viewer is not too much ported.
* You need to be able to resolve the compute nodes names (DNS or /etc/hosts)
* You need to be able to connect as root (change in vview if other user are allowed) via ssh to the compute nodes.


## keystone-simulation
----------------------
There is a weird bug somewhere in or keystone installation and this script is to debug the network connections and trace de responses. The script starts an HTTP server which responds every other time with HTTP/1.1 200 an HTTP/1.1 300 -- Only the 200 reaches the client. You simply need to run the script and it starts serving in port 4728. 

You can access the server with any curl:

 curl http://SERVER_HOST:4728


