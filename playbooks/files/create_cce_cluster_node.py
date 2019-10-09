#!/usr/bin/env python3
import sys
import time
import openstack
from otcextensions import sdk

openstack.enable_logging(True, http_debug=True)

cluster_name = sys.argv[1]
cluster_node_name = sys.argv[2]
ssh_keypair = sys.argv[3]

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)

nodeparams = {
	'kind' : 'Node',
        'apiversion' : 'v3',
        'metadata' : {
            'name' : cluster_node_name
            },
        'spec' : {
            'flavor' : 's2.large.2',
            'az' : 'eu-de-01',
            'login' : {
                'sshKey' : ssh_keypair
                },
               'rootVolume' : {
                'size' : 40,
                'volumeType' : 'SATA'
                },
            'dataVolumes' : [
                {
                'size' : 100,
                'volumetype' : 'SATA'
                }
                ],
            'count' : 1
            }
}


cluster = conn.cce.find_cluster(cluster_name)
clusternode = conn.cce.create_cluster_node(cluster, **nodeparams)
time.sleep(360)
#TBD wait function
#conn.cce.wait_for_cluster(clusternode, interval=20, wait=1200)
#wait_for_job_completion()






