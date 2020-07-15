# update ubuntu release 16.04 LTS to 18.04 LTS
## **procedure**
```console
sudo apt update && sudo apt upgrade && sudo apt dist-upgrade && sudo apt autoremove
sudo reboot now
sudo apt install update-manager-core
sudo nano /etc/update-manager/release-upgrades
modify Prompt=lts
sudo do-release-upgrade
```
## **issue**
corrupted python3(/usr/bin/python3 symlink)
```console
ctenhank@device:/usr/bin$ sudo do-release-upgrade
Checking for a new Ubuntu release
Get:1 Upgrade tool signature [819 B]                                                                   
Get:2 Upgrade tool [1,242 kB]                                                                          
Fetched 1,243 kB in 6s (195 kB/s)                                                                      
authenticate 'bionic.tar.gz' against 'bionic.tar.gz.gpg' 
extracting 'bionic.tar.gz'

Reading cache

Checking package manager

Can not upgrade 

Your python3 install is corrupted. Please fix the '/usr/bin/python3' 
symlink. 

```

## **solution**
1. update-alternatives
```console
ctenhank@device:/usr/bin$ update-alternatives --display python
python3 - auto mode
  link best version is /usr/bin/python3.5
  link currently points to /usr/bin/python3.5
  link python3 is /usr/bin/python3
/usr/bin/python3.5 - priority 1
/usr/lib/python3.7.8/python - priority 1

```
2. reinstall python
