#!/bin/bash
service ssh start
chown -R developer:developer /home/developer
su - developer -c "vncserver :1 -geometry 1280x800 -depth 24 -SecurityTypes VncAuth -xstartup /home/developer/.vnc/xstartup"
tail -f /dev/null