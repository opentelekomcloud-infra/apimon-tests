#!/usr/bin/python

from ansible.module_utils.apimon_module import ApimonModule

import requests

DOCUMENTATION = r'''
---
module: apimon_latency
version_added: 1.0.0
author: "Artem Goncharov"
options:
    hosts:
        description: Hosts list
        type: list
        required: true
    timeout:
        description: Query timeout
        type: int
        default=5
requirements: [requests]
'''

EXAMPLES = r'''
- name: Perform 'curl' query
  apimon_latency:
    hosts:
        - test.com
        - record: test2.com
          name: test2
'''

RETURN = r'''
'''


class ApimonLatency(ApimonModule):
    argument_spec = dict(
        hosts=dict(type='list', required=True),
        timeout=dict(type='int', default=5)
    )
    module_kwargs = {
        'supports_check_mode': True
    }

    def perform_request(self, host, name, timeout):
        result = None
        try:
            rsp = requests.get(host, timeout=timeout)
            duration = rsp.elapsed.total_seconds() * 1000
            metric_name = 'curl.%s.%s' % (name, str(rsp.status_code))
            metric = dict(
                name=metric_name,
                value=duration,
                metric_type='ms',
                __type='metric'
            )
            if rsp.status_code < 400:
                result = 'request took %sms and returned status_code=%s' % (
                    duration, rsp.status_code)
            else:
                self.error_occured = True
                result = 'returned %s: %s' % (
                    rsp.status_code, rsp.text)
        except requests.exceptions.ConnectionError as ex:
            metric = dict(
                name='%s.failed' % (metric_name),
                metric_type='c',
                __type='metric'
            )
            self.error_occured = True
            result = '%s' % ex

        self.metrics.append(metric)

        return result

    def run(self):

        result = dict(messages={})
        self.metrics = []
        self.error_occured = False

        for host in self.params['hosts']:
            if isinstance(host, dict):
                domain = host.get('host')
                name = host.get('name', domain.split('.')[0])
            else:
                domain = host
                name = domain.split('.')[0]
            result['messages'][domain] = self.perform_request(
                domain, name, self.params['timeout'])

        if self.metrics and self.params['socket']:
            self.emit_metrics(self.metrics, self.params['socket'])

        result['metrics'] = self.metrics

        if not self.error_occured:
            self.exit(**result)
        else:
            self.fail(msg='failure', **result)


def main():
    module = ApimonLatency()
    module()


if __name__ == '__main__':
    main()
