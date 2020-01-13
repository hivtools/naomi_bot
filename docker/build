#!/usr/bin/env bash
set -e

git_id=$(git rev-parse --short=7 HEAD)
git_branch=$(git symbolic-ref --short HEAD)

pip3 install --quiet -r requirements.txt
python3 -m pytest

registry=docker.montagu.dide.ic.ac.uk:5000
name=naomi_bot

commit_tag=$registry/$name:$git_id
branch_tag=$registry/$name:$git_branch

docker build -t $commit_tag -t $branch_tag -f docker/Dockerfile .
docker push $commit_tag
docker push $branch_tag