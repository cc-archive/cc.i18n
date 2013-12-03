#!/bin/bash

# Stupid git updater
# 
# Written in 2011 by Christopher Allan Webber, Creative Commons
# 
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty.
# 
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

CWD=`pwd`
cd "$( dirname "${BASH_SOURCE[0]}" )/.."

if [ ! -d checkouts ]; then
    mkdir checkouts
fi
    
cd checkouts    

function make_or_update_checkout
{
    DIRNAME=$1
    URL=$2

    if [ ! -d $DIRNAME ]; then
        echo "-- Cloning into $DIRNAME --"
        git clone $URL $DIRNAME
    else
        echo "-- Updating $DIRNAME --"
        cd $DIRNAME
        git checkout master
        git pull
        cd ..
    fi
}

make_or_update_checkout cc.engine https://github.com/creativecommons/cc.engine.git
make_or_update_checkout cc.license https://github.com/creativecommons/cc.license.git
make_or_update_checkout cc.licenserdf https://github.com/creativecommons/license.rdf.git
make_or_update_checkout cc.deedscraper https://github.com/creativecommons/deedscraper.git

cd "${CWD}"
