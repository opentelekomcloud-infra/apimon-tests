#!/usr/bin/env python3
import sys
import openstack
import json
from otcextensions import sdk


def find_latest_version(datastores):
    max_version = max(datastores, key=lambda x: float(x["name"]))
    return max_version["name"]


def find_smallest_flavor(flavors, az):
    # Initialize variables to track the smallest flavor
    smallest_flavor = None
    smallest_vcpus = float('inf')

    for flavor in flavors:
        vcpus = int(flavor['vcpus'])
        az_status = flavor.get('az_status', {})

        # Check if the flavor has the desired az
        if az_status.get(az) == "normal":
            # Compare the vcpus to find the smallest
            if vcpus < smallest_vcpus:
                smallest_vcpus = vcpus
                smallest_flavor = flavor['spec_code']
                group_type = flavor['group_type']

    return smallest_flavor, group_type


if __name__ == "__main__":
    try:
        if len(sys.argv) != 5:
            print(json.dumps({"error": "Invalid arguments passed"}))
            sys.exit(1)

        # Replace placeholders with actual values
        database_name = sys.argv[1]
        db_versions = json.loads(sys.argv[2])
        flavors = json.loads(sys.argv[3])
        az = sys.argv[4]

        latest_version = find_latest_version(db_versions)
        smallest_flavor, group_type = find_smallest_flavor(flavors, az)

        # Establish a connection using your OpenStack profile
        conn = openstack.connect()
        sdk.register_otc_extensions(conn)

        # Retrieve region name
        region_name = conn.config.region_name

        storage_types = list(conn.rdsv3.storage_types(
            datastore_name=database_name,
            version_name=latest_version
            ))

        # Initialize storage_type variable
        storage_type = None

        # Iterate over storage types in data1
        for storage in storage_types:
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
                    "smallest_flavor": smallest_flavor,
                }
            )
        )

    except Exception as e:
        # Always return JSON even in case of errors
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
