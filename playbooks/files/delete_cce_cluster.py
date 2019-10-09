#!/usr/bin/env python3
import sys
import openstack
from otcextensions import sdk

#openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)

cluster = conn.cce.find_cluster(sys.argv[1])
conn.cce.delete_cluster(cluster)

#TBD wait for delete
#during delete the CCE cluster first gets status Deleting, 
#then the API returns 500 Server error and last it returns no cluster found
#might be the best would be to have job querying instead of the object itself
#
#conn.cce.wait_for_delete(cluster,interval=60)
#wait_for_job_completion()
