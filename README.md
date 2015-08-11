# openstack-tools
Some easy tools to interact or do things with openstack.

simple_token.py
----------------
Once set the variables "OS_USERNAME", "OS_PASSWORD" and "OS_AUTH_URL" it gets one token for each Tenant. The response is given in 
pairs:
<tenant> <token>

    usage: simple_token.py

This script uses http requests. It is known to work in Juno version

backup_os
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

= Known Issues:
* The regular expression to extract the database parameters is quite simple, and needs to be heavily improved in order to be able to access more databases.
