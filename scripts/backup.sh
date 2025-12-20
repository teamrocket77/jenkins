#! /usr/bin/env bash
source volume.sh

docker run --rm --volumes-from jenkins -v $(pwd)/backup:/backup ubuntu tar cvf /backup/backup.tar /var/jenkins_home
