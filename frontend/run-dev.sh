#!/usr/bin/env bash

cd "$(dirname "$0")"

# install dependencies
yarn install

# run development server
yarn dev