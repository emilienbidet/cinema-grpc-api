#!/bin/bash

services=(booking movie showtime)

for service in ${services[*]}
do
  python3 $service/$service.py
done