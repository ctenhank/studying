# Building NAS Server 

## Motivation

We need some large storage for data in the lab and provide university students for assignments, and etc.

## Building Sequences

### Installation OS

We install the OS, [OMV(OpenMediaVault)](https://www.openmediavault.org/) and version is `5.x`.

1. Enter https://www.openmediavault.org/

2. Enter [Download] in the URL

3. You can download a `.iso` file in the section [ISO]

   > the link is here: https://sourceforge.net/projects/openmediavault/files/

4. You can download any version

   > I downloaded the latest version, `5.5.11`

### Building Booting Disk

And then we need to build a booting disk using the installed `.iso` file.

#### Needs:

- USB
- OS File
- Building application for booting usb`

#### My system is below:

```bash
$ uname -a
Linux host 5.4.0-53-generic #59-Ubuntu SMP Wed Oct 21 09:38:44 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
```

1. I used the OS built-in application **Startup Disk Creation**
2. If you run the application, you can do it

### Install the OS in the NAS Server

There are good references for installing the OVM for the NAS Server. 

These are Koeran, so if you can’t use the references, you can find other references in Google.

#### References:

**Installing**: https://justflight.tistory.com/65?category=416296

**Initial Setting:** https://justflight.tistory.com/66?category=416296

**Manage Repositories:** https://justflight.tistory.com/67?category=416296

**Sharing Folder:** https://justflight.tistory.com/68?category=416296

**Add-on:** https://justflight.tistory.com/70?category=416296



## Problmes

### Failed to create a file system

This message is called when I partitioned a ssd card for booting device.

Solution: [link](./problems/1.md)

