#!/usr/bin/env python3

import openstack
from otcextensions import sdk

#openstack.enable_logging(debug=True)

conn = openstack.connect()
sdk.register_otc_extensions(conn)

project_id=conn.auth['project_id']
endpoints_pair=dict(sorted((
    conn.identity.get_service(endpoint.service_id).type,
    endpoint.url.replace('$(tenant_id)s', project_id))
    for endpoint in conn.identity.endpoints()))
for service,endpoint in endpoints_pair.items():
    print(service)
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

