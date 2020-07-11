# Intermittent Disconnection Network
**Solution 1.**
```
sudo gedit /etc/default/avahi-daemon
```
Change value of variable ' AVAHI_DAEMON_DETECT_LOCAL from 1 to 0.
```
AVAHI_DAEMON_DETECT_LOCAL=1 -> AVAHI_DAEMON_DETECT_LOCAL=1
```

***Q. What's the avahi-daemon?***

Solution 2.
