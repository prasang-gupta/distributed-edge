#!/bin/bash

function downloadfile {
    wget --quiet --show-progress --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://docs.google.com/uc?export=download&id=$1" -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=$1" -O $2 && rm -rf /tmp/cookies.txt
}

mkdir -p models

downloadfile 1tfColh29wmmpSOZ6GqMTiToszibyaZcR models/efficientdet.tar.gz
downloadfile 1OaMAm5e686ABlDTpdx7FWnBJYGHvj1l2 models/faster_rcnn_v2.tar.gz
downloadfile 19cEHcZZjD3TiGg2ju7Gfnko02n3BBJk- models/ssd.tar.gz

echo "Extracting model files ..."
tar -xf models/efficientdet.tar.gz -C models
tar -xf models/faster_rcnn_v2.tar.gz -C models
tar -xf models/ssd.tar.gz -C models

echo "Cleaning up tars ..."
rm -rf models/efficientdet.tar.gz models/faster_rcnn_v2.tar.gz models/ssd.tar.gz