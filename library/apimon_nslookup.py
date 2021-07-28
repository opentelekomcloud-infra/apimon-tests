#!/usr/bin/python

from ansible.module_utils.apimon_module import ApimonModule

import socket
import time

import dns.resolver
import dns.exception
__metaclass__ = type

DOCUMENTATION = r'''
---
module: apimon_nslookup
version_added: 1.0.0
author: "Artem Goncharov"
options:
    ns_servers:
        description: NS servers to query from
        type: list
        required: true
    records:
        description: Records to query from NS servers
        type: list
        required: true
requirements: [dns]
'''

EXAMPLES = r'''
- name: Perform nslookup for public DNS servers
  apimon_nslookup:
    ns_servers: "{{ nslookup_public.ns_servers }}"
   records: "{{ nslookup_public.records }}"
'''

RETURN = r'''
'''


class ApimonNsLookup(ApimonModule):
    argument_spec = dict(
        ns_servers=dict(type='list', required=True),
        records=dict(type='list', required=True)
    )
    module_kwargs = {
        'supports_check_mode': True
    }

    def query_records(self, ns, ns_ip, records):
        results = []

        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [ns_ip]
        ns_name = self.normalize_statsd_name(ns)

        for rec in records:
            if isinstance(rec, dict):
                record = rec.get('record')
                name = self.normalize_statsd_name(
                    rec.get('name', record.split('.')[0]))
            else:
                record = rec
                name = self.normalize_statsd_name(
                    record.split('.')[0])
            try:
                start = time.perf_counter()
                answer = resolver.resolve(record, 'A')
                duration_ms = (time.perf_counter() - start) * 1000
                metric = dict(
                    name='dns.%s.%s' % (
                        ns_name,
                        name),
                    value=duration_ms,
                    metric_type='ms',
                    __type='metric'
                )

                results.append('%s (took %s ms)' % (
                    str(answer.rrset), duration_ms))
            except dns.exception.DNSException as ex:
                metric = dict(
                    name='dns.%s.%s.failed' % (
                        ns_name,
                        name),
                    value=1,
                    metric_type='c',
                    __type='metric'
                )
                self.error_occured = True
                results.append('%s' % str(ex))

            self.metrics.append(metric)

        return results

    def run(self):

        result = dict(records={})
        self.error_occured = False

        self.metrics = []

        for ns in self.params['ns_servers']:
            ns_ip = socket.gethostbyname(ns)
            records = self.query_records(
                ns, ns_ip, self.params['records'])
            result['records'][ns] = records

        if self.metrics and self.params['socket']:
            self.emit_metrics(self.metrics, self.params['socket'])

        result['metrics'] = self.metrics

        if not self.error_occured:
            self.exit(**result)
        else:
            self.fail(msg='failure', **result)


def main():
    module = ApimonNsLookup()
    module()


if __name__ == '__main__':
    main()
