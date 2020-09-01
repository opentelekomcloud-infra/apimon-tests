#!/usr/bin/env python3

import openstack


conn = openstack.connect()

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
            },
            "scope": {
                "project": {
                    "name": conn.auth['project_name']
                }
            }
        }
    }
)

token_id = token.headers['X-Subject-Token']

token_from_token = conn.identity.post(
    '/auth/tokens',
    json={
        "auth": {
            "identity": {
                 "methods": ["token"],
                 "token": {
                     "id": token_id
                 }
            },
            "scope": {
               "project": {
                   "name": conn.auth['project_name']
               }
              }
          }
    },
    headers={
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'openstacksdk/0.48.1 keystoneauth1/4.2.1 '
                      'python-requests/2.23.0 CPython/3.8.5',
        'X-Auth-Token': token_id
    }
)

token_from_token_id = token_from_token.headers['X-Subject-Token']

conn.identity.delete(
    '/auth/tokens',
    headers={
        'X-Auth-Token': token_from_token_id,
        'X-Subject-Token': token_from_token_id
    }
)

conn.identity.delete(
    '/auth/tokens',
    headers={
        'X-Auth-Token': token_id,
        'X-Subject-Token': token_id
    }
)
