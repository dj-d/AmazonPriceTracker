#!/bin/bash

# OS and Package manager variables
os="$(awk -F= '/^NAME/{print $2}' /etc/os-release)"
YUM_CMD="$(which yum)"
PACMAN_CMD="$(which pacman)"
APT_CMD="$(which apt)"
APT_GET_CMD="$(which apt-get)"

# TODO
function docker_installer() {
    sudo usermod -aG docker $(whoami)
}

# OS check
echo "----- Running System: ${os} -----"

# Package manager check
if [[ ! -z $YUM_CMD ]]; then
        echo "----- YUM Dependencies: -----"
        # TODO

elif [[ ! -z $PACMAN_CMD ]]; then
        echo "----- PACMAN Dependencies: -----"
        # TODO

elif [[ ! -z $APT_CMD ]]; then
        echo "----- APT manager Dependencies -----"
        sudo apt install jq

elif [[ ! -z $APT_GET_CMD ]]; then
        echo "----- APT-GET manager Dependencies -----"
        sudo apt-get install jq

else
        # No available package manager
        echo "Error can't install dependencies, no YUM or PACMAN or APT or APT-GET manager installed"
        exit 1;
fi

exit