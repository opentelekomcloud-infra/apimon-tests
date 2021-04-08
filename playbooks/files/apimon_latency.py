#!/usr/bin/env python3

import json
import os
import requests
import socket
import sys


def serialize_metric(msg):
    try:
        return json.dumps(msg, separators=(',', ':'))
    except json.JSONDecodeError as err:
        return err.msg


def emit_metric(socket_name, metric):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as _socket:
        _socket.connect(socket_name)
        msg = '%s\n' % serialize_metric(metric)
        _socket.sendall(msg.encode('utf8'))


def main():
    host = sys.argv[1]
    metric_name = 'curl.%s' % sys.argv[2]
    if len(sys.argv) == 4:
        request_timeout = int(sys.argv[3])
    else:
        request_timeout = 5
    socket = os.getenv('APIMON_PROFILER_MESSAGE_SOCKET')
    duration = -1
    try:
        rsp = requests.get(host, timeout=request_timeout)
        duration = rsp.elapsed.total_seconds() * 1000
        metric_name = '%s.%s' % (metric_name, str(rsp.status_code))
        metric = dict(
            name=metric_name,
            value=duration,
            metric_type='ms',
            __type='metric'
        )
    except requests.exceptions.ConnectionError:
        metric = dict(
            name='%s.failed' % (metric_name),
            metric_type='c',
            __type='metric'
        )

    emit_metric(socket, metric)


main()
