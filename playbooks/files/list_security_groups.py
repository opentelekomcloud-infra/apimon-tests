#!/usr/bin/env python3

import openstack
import logging

conn = openstack.connect()

list(conn.network.security_groups())
list(conn.network.security_group_rules())
