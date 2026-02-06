#!/usr/bin/env python3

import openstack
import sys
from otcextensions import sdk
from openstack import exceptions as os_exc

statuses = ['creating', 'restoring', 'deleting']

conn = openstack.connect()
sdk.register_otc_extensions(conn)

vault_found = False
for vault in conn.cbr.vaults(name=sys.argv[1]):
    if vault.billing.get('status') in statuses:
        for count in openstack.utils.iterate_timeout(
                timeout=1200, message='Wait for backup status failed',
                wait=5):
            try:
                vault = conn.cbr.get_vault(vault.id)
            except os_exc.ResourceNotFound:   # Excepction when the Vault was already deleted 
                break

            if vault.billing.get('status') not in statuses:
                break

    vault_found = True

    # CBR Vault delete
    try:
        conn.cbr.delete_vault(vault.id)
        print(f"Vault {vault.id} delete requested")

    except os_exc.ResourceNotFound:
        print("Vault already deleted")

    except os_exc.BadRequestException as e:
        #  Exception when the vault was already deleted
        if "BackupService.6203" in str(e):
            print("Vault already deleted / invalid state – ignoring")
        else:
            raise

    break


if not vault_found:
    print("No vault found with that name")
