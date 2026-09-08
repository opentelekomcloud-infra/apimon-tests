#!/usr/bin/env python3

import re
import sys

import openstack
from otcextensions import sdk

# openstack.enable_logging(True, http_debug=True)

# An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
conn = openstack.connect()

# Register OTC Extensions
sdk.register_otc_extensions(conn)

# Search for corresponding cluster
cluster = conn.cce.find_cluster(sys.argv[1])

# Query Certificate information
certificates = conn.cce.get_cluster_certificates(cluster)

# Use RegEx to create kubectl conform configuration information
ca_regex = r"ca=(\w*\={,2}),"
client_certificate_regex = r"client_certificate=(\w*\={,2}),"
client_key_regex = r"client_key=(\w*\={,2}),"
internal_ip_regex = r"context={'name': 'internal', 'cluster': 'https://((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]):[0-9]{,5})"

ca_data = re.search(ca_regex, str(certificates))
client_certificate_data = re.search(client_certificate_regex,
                                    str(certificates))
client_key_data = re.search(client_key_regex, str(certificates))
internal_ip_data = re.search(internal_ip_regex, str(certificates))

ca_data = ca_data.group(1)
client_certificate_data = client_certificate_data.group(1)
client_key_data = client_key_data.group(1)
internal_ip_data = "https://" + internal_ip_data.group(1)

# print("CA-data: " + ca_data)
# print("Client Cert Data: " + client_certificate_data)
# print("Client Key Data: " + client_key_data)
# print("IP Data: " + internal_ip_data)

kube_config = {
        "kind": "Config",
        "apiVersion": "v1",
        "preferences": {
        },
        "clusters": [
            {
                "name": "internalCluster",
                "cluster": {
                    "server": internal_ip_data,
                    "certificate-authority-data": ca_data
                    }
            }
        ],
        "users": [
            {
                "name": "user",
                "user": {
                    "client-certificate-data": client_certificate_data,
                    "client-key-data": client_key_data
                }
            }
        ],
        "contexts": [
            {
                "name": "internal",
                "context": {
                    "cluster": "internalCluster",
                    "user": "user"
                }
            }
        ],
        "current-context": "internal"
}

print(str(kube_config))
