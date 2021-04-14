#!/usr/bin/python


from ansible.module_utils.basic import AnsibleModule

import abc
import json
import os
import socket


def message_full_argument_spec(**kwargs):
    spec = dict(
        socket=dict(default=os.getenv("APIMON_PROFILER_MESSAGE_SOCKET", ""))
    )
    spec.update(kwargs)
    return spec


class ApimonModule:
    argument_spec = {}
    module_kwargs = {}

    def __init__(self):

        self.ansible = AnsibleModule(
            message_full_argument_spec(**self.argument_spec),
            **self.module_kwargs)
        self.params = self.ansible.params
        self.module_name = self.ansible._name
        self.results = {'changed': False}
        self.exit = self.exit_json = self.ansible.exit_json
        self.fail = self.fail_json = self.ansible.fail_json

    @abc.abstractmethod
    def run(self):
        pass

    def __call__(self):
        """Execute `run` function when calling the instance.
        """

        try:
            results = self.run()
            if results and isinstance(results, dict):
                self.ansible.exit_json(**results)

        except Exception as e:
            self.ansible.fail_json(msg=str(e))

    @staticmethod
    def serialize(msg):
        """Serialize data as json string"""
        try:
            return json.dumps(msg, separators=(',', ':'))
        except json.JSONDecodeError as err:
            return err.msg

    def emit_metric(self, data, message_socket):
        """push single metrics to socket"""
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as _socket:
            try:
                _socket.connect(message_socket)
                msg = '%s\n' % self.serialize(data)
                _socket.send(msg.encode('utf8'))
            except socket.error as err:
                self.ansible.fail_json(
                    msg='error establishing connection to socket')
                raise err
            except Exception as ex:
                self.ansible.fail_json(
                    msg='error writing message to socket')
                raise ex

    def emit_metrics(self, metrics, message_socket):
        """Emit array of metrics into the socket"""
        for data in metrics:
            self.emit_metric(data, message_socket)

    @staticmethod
    def normalize_statsd_name(name):
        name = name.replace('.', '_')
        name = name.replace(':', '_')
        return name
