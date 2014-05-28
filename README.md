flow\_buildbot
=============

Buildbot plugin for Velocity Flow

Installation
------------

To install this plugin on the Velocity Flow platform, either download a tar file
and extract the files or use git clone to any directory.

Next the following to the /etc/cato/legato.yaml configuration file.
Make sure to change the path and buildbot server address.

Note: If the "plugins:" directive already exists, skip it and add the "buildbot:" 
directive below with the path and url settings.
```
plugins:
    buildbot:
        path: /home/username/flow_buildbot
        url: http://serveraddress:8010 
```

Now restart the Flow (legato) services.
```
$CSK_HOME/legato/services/restart_services.sh
```
