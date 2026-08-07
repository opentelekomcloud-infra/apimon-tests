#!/usr/bin/env python3

import openstack

from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect()
sdk.register_otc_extensions(conn)

list(conn.obs.containers())
