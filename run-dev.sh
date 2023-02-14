#!/usr/bin/env bash

# run mongodb container
./mongo_container/run-dev.sh

# run API backend
./backend/run-dev.sh&

# run webUI frontend
./frontend/run-dev.sh&