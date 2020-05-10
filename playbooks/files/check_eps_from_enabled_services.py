#!/usr/bin/env python3

import openstack
from otcextensions import sdk

#openstack.enable_logging(debug=True)

conn = openstack.connect()
sdk.register_otc_extensions(conn)

for service in conn.config.get_enabled_services():
    print(service)
    resp=None
    timeout=False
    service=service.replace('_', '-')
    try:
        resp=conn.compute.get_endpoint(service_type=service)
    except:
        timeout=True
        print(service, '-', 'error')
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

