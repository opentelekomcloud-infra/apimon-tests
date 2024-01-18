#!/usr/bin/env python3

import openstack

conn = openstack.connect()

for az in conn.dcs.availability_zones():
  print(az.name)
