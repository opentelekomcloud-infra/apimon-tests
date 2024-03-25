#!/usr/bin/env python3

import sys

import openstack
from otcextensions import sdk

# openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)

cluster = conn.cce.find_cluster(sys.argv[1])
node = conn.cce.find_cluster_node(cluster, sys.argv[2])
dict = {
    "metadata": {
        "name": sys.argv[2]
    },
    "spec": {
        "flavor": "s2.large.4",
        "az": "eu-de-01",
        "login": {
            "sshKey": sys.argv[3]
        },
        "rootVolume": {
            "size": 40,
            "volumetype": "SATA"
        },
        "dataVolumes": [
            {
                "size": 100,
                "volumetype": "SATA"
            }
        ],
        "count": 1
    }
}

if cluster and (node is None):
    node = conn.cce.create_cluster_node(cluster, **dict)
    job = conn.cce.get_job(node.job_id)
    conn.cce.wait_for_job(job)
