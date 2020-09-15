#!/usr/bin/env python3

import time
import openstack
from openstack import exceptions


def get_token_from_password(conn):
    response = conn.identity.post(
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
    exceptions.raise_from_response(response)
    return (response.headers['X-Subject-Token'], response.json())


def get_token_from_token(conn, token_id):
    response = conn.identity.post(
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
    exceptions.raise_from_response(response)
    return (response.headers['X-Subject-Token'], response.json())


def revoke_token(conn, token):
    response = conn.identity.delete(
        '/auth/tokens',
        headers={
            'X-Auth-Token': token,
            'X-Subject-Token': token
        }
    )
    exceptions.raise_from_response(response)


def dummy_get(conn, token):
    response = conn.compute.get(
        '/servers',
        headers={
            'X-Auth-Token': token,
        }
    )
    exceptions.raise_from_response(response)


def main():
    openstack.enable_logging(debug=True)
    conn = openstack.connect()

    token1_id, rsp = get_token_from_password(conn)
    token1_from_token_id, rsp = get_token_from_token(conn, token1_id)

    token2_id, rsp = get_token_from_password(conn)
    token2_from_token_id, rsp = get_token_from_token(conn, token2_id)

    # Ensure
    dummy_get(conn, token1_id)
    dummy_get(conn, token2_id)
    dummy_get(conn, token1_from_token_id)
    dummy_get(conn, token2_from_token_id)
    # Ensure we can stil get another token from 1st token
    #token3_from_token_id, rsp = get_token_from_token(conn, token1_id)

    #revoke_token(conn, token3_from_token_id)
    revoke_token(conn, token2_from_token_id)
    revoke_token(conn, token1_from_token_id)
    revoke_token(conn, token2_id)
    revoke_token(conn, token1_id)
    time.sleep(2)

    dummy_get(conn, token1_id)


if __name__ == "__main__":
    main()
