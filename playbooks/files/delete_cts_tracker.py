#!/usr/bin/env python3

import openstack

conn = openstack.connect()
conn.cts.delete_tracker()
