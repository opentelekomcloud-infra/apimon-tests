#!/usr/bin/env python3
import sys
import openstack
import json
from otcextensions import sdk


def find_latest_version(datastores):
    max_version = max(datastores, key=lambda x: float(x["name"]))
    return max_version["name"]


if __name__ == "__main__":
    try:
        if len(sys.argv) != 4:
            print(json.dumps({"error": "check_rds_flavor.py <flavor_code>"}))
            sys.exit(1)

        # Replace placeholders with actual values
        database_name = sys.argv[1]
        db_versions = json.loads(sys.argv[2])
        spec_code = sys.argv[3]

        latest_version = find_latest_version(db_versions)

        # Establish a connection using your OpenStack profile
        conn = openstack.connect()
        sdk.register_otc_extensions(conn)

        # Determine the service type and interface
        service_type = "rdsv3"  # Adjust this to match your service
        interface = "public"  # Use 'internal' or 'admin' if necessary

        # Retrieve the service endpoint
        endpoint = conn.session.get_endpoint(
            service_type=service_type, interface=interface
        )

        # Retrieve region name
        region_name = conn.config.region_name

        # Construct the URL
        url1 = (
            f"{endpoint}/storage-type/{database_name}"
            f"?version_name={latest_version}"
        )

        # Make the GET request using the authenticated session
        response = conn.session.get(url1)
        data1 = response.json()

        flavors = conn.rdsv3.flavors(
            datastore_name=database_name,
            version_name=latest_version,
            spec_code=spec_code,
        )
        flavor_list = list(flavors)
        group_type = flavor_list[0].group_type

        # Initialize storage_type variable
        storage_type = None

        # Iterate over storage types in data1
        for storage in data1["storage_type"]:
            if group_type in storage["support_compute_group_type"]:
                storage_type = storage["name"]
                if storage_type == "COMMON":
                    continue
                break  # Exit the loop after finding the first match

        # Output the result as JSON
        print(
            json.dumps(
                {
                    "region": region_name,
                    "storage_type": storage_type,
                    "latest_version": latest_version,
                }
            )
        )

    except Exception as e:
        print(f"Error: {str(e)}")
