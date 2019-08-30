#!/usr/bin/env python3

import openstack
import logging


conn = openstack.connect()

list(conn.compute.keypairs())
