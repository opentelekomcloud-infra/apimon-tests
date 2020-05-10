#!/usr/bin/env python3

import openstack
from otcextensions import sdk
from keystoneauth1 import exceptions

#openstack.enable_logging(debug=True)

conn = openstack.connect()
sdk.register_otc_extensions(conn)

for service,data in conn.config.get_service_catalog().get_endpoints().items():
    print(service)
    endpoint=data[0]['url']
    print(endpoint)
    resp=None
    timeout=False
    try:
        resp=conn.compute.get(endpoint,
                              headers={'content-type': 'application/json'})
    except:
        timeout=True
        print(endpoint, '-', 'error')
    if timeout:
        data = [dict(
            measurement=(
                conn.compute._influxdb_config.get('measurement',
                                                  'openstack_api')
                if conn.compute._influxdb_config else 'openstack_api'
            ),
            tags=dict(
                method='GET',
                service_type=service,
                status_code='-1',
                name=service
            ),
            fields=dict(
                duration=5,
                status_code_val=-1
            )
        )]
        try:
            print(data)
            conn.compute._influxdb_client.write_points(data)
        except Exception:
            conn.compute.log.exception('Error writing statistics to InfluxDB')

