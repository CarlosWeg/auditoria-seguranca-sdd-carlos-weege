#!/bin/bash
set -euxo pipefail

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y docker.io
systemctl enable docker
systemctl start docker

mkdir -p /opt/minirisk
chown ubuntu:ubuntu /opt/minirisk
usermod -aG docker ubuntu
