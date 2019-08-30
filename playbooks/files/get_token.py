#!/usr/bin/env python3

import openstack
import logging


conn = openstack.connect()

# logging.basicConfig(level=logging.DEBUG)
# openstack.enable_logging(debug=True, http_debug=True)

token = conn.identity.post(
    '/auth/tokens',
    json={
        "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "name": conn.auth['username'],
                    "domain": {
                        "name": conn.auth['user_domain_name']
                    },
                    "password": conn.auth['password']
                }
            }
        }
    }
    }
)
