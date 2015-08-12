# NdriveFUSE
FUSE wrapper for Naver NDrive

## Notice
This project use python wrapper for NAVER Ndrive project (https://github.com/carpedm20/ndrive) by carpedm20.

## Dependencies
- pynotify
- OSD (On Screen Display): Canonical's on-screen-display notification agent
- ghost.py
- fusepy

## Installation 
Install NdriveFUSE
```
$ python2 setup.py install
```

Copy configuration file
```
$ cp ndrivecfg_example $HOME/.ndrivecfg
```

Run key generator 
```
$ NdriveFUSE_Gen
```
   it will generate encrypted key about your naver account information
   
   **NOTICE** Encryption has not purpose on security. The main reason of
   encryption is keeping your account information from being shown easily by 
   other users.

## Usage
```
NdriveFUSE $(MOUNT_POINT)

i.e. NdriveFUSE ~/mountpoint
```

## License
GPL version 2.0

If you have any issues or need help, please mail to chaoxifer@gmail.com
