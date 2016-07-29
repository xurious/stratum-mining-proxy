stratum-mining-proxy
====================

Application providing bridge between old HTTP/getwork protocol and Stratum mining protocol
as described here: http://siamining.com/stratum.

This is a port for Sia of the original Stratum mining proxy by Slush.

Installation on Windows
-----------------------

1. Download official Windows binaries (EXE) from http://siamining.com/files/mining_proxy.exe
2. Open downloaded file. It will open console window. Using default settings, proxy connects to SiaMining's pool interface
3. If you want to connect to another pool or change other proxy settings, type "mining_proxy.exe --help" in console window.

Installation on Linux - local hierarchy
---------------------------------------

1. Download TGZ file from https://github.com/SiaMining/stratum-mining-proxy/tarball/master
2. Unpack it by typing "tar xf SiaMining-stratum-mining_proxy*.tar.gz"
3. Most likely you already have Python respectively OpenSSL installed on your system. Otherwise install it by "sudo apt-get install python-dev libssl-dev"
(on Ubuntu and Debian).
3. Type "sudo python setup.py install" in the unpacked directory.
4. You can start the proxy by typing "./mining_proxy.py" in the terminal window. Using default settings,
proxy connects to SiaMining's pool interface.
5. If you want to connect to another pool or change other proxy settings, type "mining_proxy.py --help".

Packaging for Debian
--------------------

1. Install devscripts, debhelper, pbuilder.
2. Download and unpack a tarball or clone this repository. Enter the unpacked/cloned direcotry.
3. Type "debuild-pbuilder -b -uc -us". You will be asked your password for sudo command. If you're a sudoer, skip to the last step.
4. If you're not a sudoer, an error will occur. Do `apt-get -f install' as root to correct the situation and call "debuild -b -uc -us".
5. A .deb package will be generated in parent directory. Use it to install stratum-mining-proxy on a Debian compatible system.

Installation on Mac
-------------------
1. Download TGZ file from https://github.com/SiaMining/stratum-mining-proxy/tarball/master
2. Unpack it by typing "tar xf SiaMining-stratum-mining-proxy*.tar.gz"
3. On Mac OS X you already have Python installed on your system, but you lack the llvm-gcc-4.2 binary required to run the setup.py file, so:
3. a) If you don't want to install Xcode, get gcc here: https://github.com/kennethreitz/osx-gcc-installer
3. b) OR download Xcode (free) from the App Store, Open it up (it's in your applications folder) and go to preferences, to the downloads section and download/install the 'command line tools'. This will install llvm-gc-4.2.
4. Type "sudo python setup.py install" in the unpacked directory from step 2.
5. You can start the proxy by typing "./mining_proxy.py" in the terminal window. Using default settings, proxy connects to SiaMining's pool interface.
6. If you want to connect to another pool or change other proxy settings, type "mining_proxy.py --help".

N.B. Once Apple releases Xcode 4.7 they will remove the optional install of gcc (they want you to use clang). When that happens you can either choose not to upgrade, or return to the aforementioned https://github.com/kennethreitz/osx-gcc-installer and download the specific gcc binary for your version of Mac OS.

Installation on Linux using Git
-------------------------------
This is advanced option for experienced users, but give you the easiest way for updating the proxy.

1. git clone git://github.com/SiaMining/stratum-mining-proxy.git
2. cd stratum-mining-proxy
3. sudo apt-get install python-dev # Development package of Python are necessary
4. sudo python setup.py develop # This will install required dependencies (namely Twisted and Stratum libraries),
but don't install the package into the system.
5. You can start the proxy by typing "./mining_proxy.py" in the terminal window. Using default settings,
proxy connects to SiaMining's pool interface.
6. If you want to connect to another pool or change other proxy settings, type "./mining_proxy.py --help".
7. If you want to update the proxy, type "git pull" in the package directory.

Contact
-------

This proxy is provided by SiaMining mining pool at http://siamining.com. You can contact the author
by email dev(at)siamining.com.
