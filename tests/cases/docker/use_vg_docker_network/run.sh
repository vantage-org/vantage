#!/bin/sh
vantage --var VG_DOCKER_NETWORK=vantagetestusesnetwork do-something
docker inspect use_vg_docker_network -f "{{json .NetworkSettings.Networks.vantagetestusesnetwork.NetworkID }}"
docker stop use_vg_docker_network
docker rm use_vg_docker_network
docker network rm vantagetestusesnetwork
