#!/bin/sh
vantage --var VG_DOCKER_NETWORK=vantagetestusesnetwork do-something &

docker inspect use_vg_docker_network -f "{{json .NetworkSettings.Networks.vantagetestusesnetwork.NetworkID }}"

wait

docker network rm vantagetestusesnetwork
