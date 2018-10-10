# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
	. "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# Check if using default distro password
PASS=$(sudo grep 'pi' /etc/shadow | sed -e 's/pi:\([^:]*\).*/\1/')
#echo $PASS

if [[ $PASS = *zp7VNHu2dDrGuyAESg2pFPgI8OsJae7moqkIqreIb8sgphi0rHAkOI10j7MJtumRI13Ij4DZn1slsjxxVBcoA* ]]
then
        echo "Please change your password using 'sudo /usr/bin/raspi-config'"
fi
