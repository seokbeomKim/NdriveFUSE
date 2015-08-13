# NdriveFUSE
FUSE wrapper for Naver NDrive for LINUX

**리눅스용 네이버 N드라이브**

![](https://github.com/seokbeomKim/NdriveFUSE/blob/gh-pages/screenshot_001.png)
## Notice
This project use python wrapper for NAVER Ndrive project (https://github.com/carpedm20/ndrive) by carpedm20.

## Dependencies
- setuptools (ubuntu: python-setuptools)
- clint (ubuntu: python-clint)
- simplejson (ubuntu: python-simplejson)
- magic (ubuntu: python-magic)
- pynotify (or python2-notify)
- flask (ubuntu: python-flask)
- OSD (On Screen Display): Canonical's on-screen-display notification agent
- ghost.py (http://ghostpy.readthedocs.org/en/latest/)
-- to install ghost.py, pyside should be installed (ubuntu: python-pyside)
- fusepy

## Installation
**Make sure that your system satisfy the dependencies above.**

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

## Configuration
### Synchronization
you can customize synchronization with following setting
```
# NDrive configuration
# Exclude cache
cache_exclude_directories = "/exclude_dir, /exclude_dir2"
cache_exclude_files = "/test/exclude_file1, /test/exclude_file2 /test/form_nfrm.nfrm"
cache_exclude_filetype = "a, jpg, zip, nppt, nxls"
cache_exclude_filesize = "4096"

# Default cache directory is "~/.ndrive".
cache_directory = "/home/chaoxifer/.ndrive"
```

## License
GPL version 2.0

## Copyright
Copyright 2015 Sukbeom Kim

NdriveFUSE is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
any later version.
NdriveFUSE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with NdriveFUSE.  If not, see <http://www.gnu.org/licenses/>.


If you have any issues or need help, please mail to chaoxifer@gmail.com
