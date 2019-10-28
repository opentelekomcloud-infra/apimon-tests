#!/usr/bin/env python3

import openstack
import logging

#openstack.enable_logging(debug=True, http_debug=True)

def allocate():
    conn = openstack.connect()
    network=conn.network.find_network('admin_external_net')
    fipip = conn.network.create_ip(floating_network_id=network.id)
    print(fipip.id)

allocate()
