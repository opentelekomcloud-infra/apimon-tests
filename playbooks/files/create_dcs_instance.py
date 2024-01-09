#!/usr/bin/env python3

import openstack
import sys

conn = openstack.connect()

instance_name = sys.argv[1]
vpc_id = sys.argv[2]
subnet_id = sys.argv[3]
sg_id = sys.argv[4]

instance = conn.dcs.create_instance(
    name=instance_name,
    available_zones=["eu-de-03"],
    capacity=2,
    engine="Redis",
    engine_version="3.0",
    maintain_begin="02:00:00",
    maintain_end="06:00:00",
    password="Password.123##",
    product_id="OTC_DCS_SINGLE",
    resource_spec_code="dcs.single_node",
    security_group_id=sg_id,
    subnet_id=subnet_id,
    vpc_id=vpc_id
)
#print(instance)
