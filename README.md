# gcurlftpfs

Graphical interface and tools for curlftpfs program

### Overview

**gcurlftpfs** provides a lightweight graphical user interface and tools for curlftpfs program.

It performs and manage of curlftpfs connections, even those established via command line

### Requirements

[python 2.7](http://python.org/download/)

[Tcl/Tk libs](http://www.tcl.tk/software/tcltk/download.html)

[curlftpfs](https://sourceforge.net/projects/curlftpfs/)

[fuse](https://sourceforge.net/projects/fuse/)

Mac OS X users need curlftpfs from [MacPorts](http://www.macports.org/).

### Download and version notes

Latest version: gcurlftpfs 0.2

[Download](https://github.com/claudiodangelis/gcurlftpfs/tags)

[Browse code](https://github.com/claudiodangelis/gcurlftpfs)

### Platforms

**Linux** and **Mac OS X**

### Installation and usage

You have several ways to run it:

    python gcurlftpfs.py

&nbsp;

    chmod +x gcurlftpfs.py
    ./gcurlftpfs.py

&nbsp;

    chmod +x gcurlftpfs.py
    sudo cp ./gcurlftpfs.py /usr/local/bin/gcurlftpfs
    gcurlftpfs

#### Debian

Install dependencies:

    sudo apt-get install python-tk curlftpfs


> Debian configures FUSE to require users to be in the `fuse` group, so, as root, type:
>
>    `sudo gpasswd -a yourusername fuse`

then log out and log in.

### Screenshots

![](http://claudiodangelis.com/img/posts/gcurlftpfs1.png)

    

![](http://claudiodangelis.com/img/posts/gcurlftpfs2.png)

    

![](http://claudiodangelis.com/img/posts/gcurlftpfs6.png)


### Known issues

*   There is no stable error handler implemented yet, behavior in case of error is unpredictable
*   When a connection is established, <u>**Console echoes plain-text username's password**</u>
*   on Mac OS X, **unmount** return errors, but it works fine actually


### Author(s)

Claudio d'Angelis [claudiodangelis.com/+](http://claudiodangelis.com/+)


### License

Copyright (C) 2012 Claudio Dawson d'Angelis

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    A copy of the GNU General Public License version 2 is set out below.
    You can also obtain a written copy from the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

