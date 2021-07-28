#!/usr/bin/env python3

import openstack

conn = openstack.connect()

list(conn.network.routers())
