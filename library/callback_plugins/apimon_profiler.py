# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    callback: apimon_profiler
    type: aggregate
    short_description: adds time statistics about invoked OpenStack modules
    version_added: "2.9"
    description:
      - Ansible callback plugin for timing individual APImon related tasks and
        overall execution time.
    requirements:
      - whitelist in configuration - see examples section below for details.
      - influxdb python client for writing metrics to influxdb
    options:
      influxdb_measurement:
          description: InfluxDB measurement name
          default: 'ansbile_stats'
          env:
              - name: APIMON_PROFILER_INFLUXDB_MEASUREMENT_NAME
          ini:
              - section: callback_apimon_profiler
                key: measurement_name
      influxdb_host:
          description: InfluxDB Host
          env:
              - name: APIMON_PROFILER_INFLUXDB_HOST
          ini:
              - section: callback_apimon_profiler
                key: influxdb_host
      influxdb_port:
          description: InfluxDB Port
          default: 8086
          env:
              - name: APIMON_PROFILER_INFLUXDB_PORT
          ini:
              - section: callback_apimon_profiler
                key: influxdb_port
      influxdb_user:
          description: InfluxDB User name
          env:
              - name: APIMON_PROFILER_INFLUXDB_USER
          ini:
              - section: callback_apimon_profiler
                key: influxdb_user
      influxdb_password:
          description: InfluxDB User password
          env:
              - name: APIMON_PROFILER_INFLUXDB_PASSWORD
          ini:
              - section: callback_apimon_profiler
                key: influxdb_password
      use_last_name_segment:
          description: Use only last part of the name after colon sign as name
          default: True
          type: boolean
          env:
              - name: APIMON_PROFILER_USE_LAST_NAME_SEGMENT
          ini:
              - section: callback_apimon_profiler
                key: use_last_name_segment
      alerta_endpoint:
          description: Endpoint for sending alerta alerts
          type: str
          env:
              - name: APIMON_PROFILER_ALERTA_ENDPOINT
          ini:
              - section: callback_apimon_profiler
                key: alerta_endpoint
      alerta_token:
          description: Alerta authorization token
          type: str
          env:
              - name: APIMON_PROFILER_ALERTA_TOKEN
          ini:
              - section: callback_apimon_profiler
                key: alerta_token

'''

EXAMPLES = '''
example: >
  To enable, add this to your ansible.cfg file in the defaults block
    [defaults]
    callback_whitelist = apimon_profiler
sample output: >
Monday 22 July 2019  18:06:55 +0200 (0:00:03.034)       0:00:03.034 ***********
===============================================================================
Action=os_auth, state=None duration=1.19, changed=False, name=Get Token
Action=script, state=None duration=1.48, changed=True, name=List Keypairs
Overall duration of APImon tasks in playbook playbooks/scenarios/sc1_tst.yaml
    is: 2675.616 ms
Playbook run took 0 days, 0 hours, 0 minutes, 2 seconds

'''

import collections
import logging
import os
import re
import time

from ansible.module_utils.six.moves import reduce
from ansible.module_utils._text import to_text
from ansible.plugins.callback import CallbackBase

from pathlib import PurePosixPath

try:
    import influxdb
except ImportError:
    influxdb = None

try:
    from alertaclient.api import Client as alerta_client
except ImportError:
    alerta_client = None


# define start time
t0 = tn = time.time_ns()
te = 0

rc_str_struct = {
    0: 'Passed',
    1: 'Skipped',
    2: 'FailedIgnored',
    3: 'Failed'
}


def secondsToStr(t):
    # http://bytes.com/topic/python/answers/635958-handy-short-cut-formatting-elapsed-time-floating-point-seconds
    def rediv(ll, b):
        return list(divmod(ll[0], b)) + ll[1:]

    return "%d:%02d:%02d.%03d" % tuple(
        reduce(rediv, [[t * 1000, ], 1000, 60, 60]))


def filled(msg, fchar="*"):
    if len(msg) == 0:
        width = 79
    else:
        msg = "%s " % msg
        width = 79 - len(msg)
    if width < 3:
        width = 3
    filler = fchar * width
    return "%s%s " % (msg, filler)


def timestamp(self):
    if self.current is not None:
        self.stats[self.current]['time'] = time.time() - \
                self.stats[self.current]['time']


def tasktime():
    global tn
    time_current = time.strftime('%A %d %B %Y  %H:%M:%S %z')
    time_elapsed = secondsToStr((te - tn)/1000000000)
    time_total_elapsed = secondsToStr((te - t0)/1000000000)
    tn = time.time_ns()
    return filled('%s (%s)%s%s' %
                  (time_current, time_elapsed, ' ' * 7, time_total_elapsed))


class CallbackModule(CallbackBase):
    """
    This callback module processes information about each task and report
    individual statistics into influxdb.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'apimon_profiler'
    CALLBACK_NEEDS_WHITELIST = True

    ACTION_SERVICE_MAP = {
        'os_auth': 'identity',
        'os_client_config': 'general',
        'os_flavor_info': 'compute',
        'os_floating_ip': 'network',
        'os_group': 'identity',
        'os_group_info': 'identity',
        'os_image': 'image',
        'os_image_info': 'image',
        'os_keypair': 'compute',
        'os_keystone_domain': 'identity',
        'os_keystone_domain_info': 'identity',
        'os_keystone_endpoint': 'identity',
        'os_keystone_role': 'identity',
        'os_keystone_service': 'identity',
        'os_listener': 'loadbalancer',
        'os_loadbalancer': 'loadbalancer',
        'os_member': 'loadbalancer',
        'os_network': 'network',
        'os_networks_info': 'network',
        'os_object': 'object_store',
        'os_pool': 'loadbalancer',
        'os_port': 'network',
        'os_port_info': 'network',
        'os_project': 'identity',
        'os_project_access': 'identity',
        'os_project_info': 'identity',
        'os_quota': 'quota',
        'os_recordset': 'dns',
        'os_router': 'network',
        'os_security_group': 'network',
        'os_security_group_rule': 'network',
        'os_server': 'compute',
        'os_server_action': 'compute',
        'os_server_group': 'compute',
        'os_server_info': 'compute',
        'os_server_metadata': 'compute',
        'os_server_volume': 'compute',
        'os_stack': 'orchestrate',
        'os_subnet': 'network',
        'os_subnets_info': 'network',
        'os_user': 'identity',
        'os_user_group': 'identity',
        'os_user_info': 'identity',
        'os_user_role': 'identity',
        'os_volume': 'block_storage',
        'os_volume_snapshot': 'block_storage',
        'os_zone': 'dns',
        'os_flavor_facts': 'compute',
        'os_image_facts': 'image',
        'os_keystone_domain_facts': 'identity',
        'os_networks_facts': 'network',
        'os_port_facts': 'network',
        'os_project_facts': 'identity',
        'os_server_actions': 'compute',
        'os_server_facts': 'compute',
        'os_subnets_facts': 'network',
        'os_user_facts': 'identity',
        'otc_listener': 'loadbalancer',
        'otc_loadbalancer': 'loadbalancer',
        'otc_member': 'loadbalancer',
        'otc_pool': 'loadbalancer',
        'rds_datastore_info': 'rds',
        'rds_flavor_info': 'rds'
    }

    def __init__(self):
        self.stats = collections.OrderedDict()
        self.current = None
        self.playbook_name = None
        self.influxdb_client = None

        super(CallbackModule, self).__init__()

    def set_options(self, task_keys=None, var_options=None, direct=None):

        super(CallbackModule, self).set_options(task_keys=task_keys,
                                                var_options=var_options,
                                                direct=direct)

        self.measurement_name = self.get_option('influxdb_measurement')

        if influxdb:
            self.influxdb_host = self.get_option('influxdb_host')
            self.influxdb_port = self.get_option('influxdb_port')
            self.influxdb_user = self.get_option('influxdb_user')
            self.influxdb_password = self.get_option('influxdb_password')

            try:
                self.influxdb_client = influxdb.InfluxDBClient(
                    self.influxdb_host,
                    self.influxdb_port,
                    self.influxdb_user,
                    self.influxdb_password
                )
                self._display.vv('Established InfluxDB connection')
            except Exception as e:
                self._display.warning('Profiler: Cannot establish DB '
                                      'connection: %s' % e)
        else:
            self._display.warning('InfluxDB python client is not available')

        if alerta_client:
            self.alerta_ep = self.get_option('alerta_endpoint')
            self.alerta_token = self.get_option('alerta_token')
            self.alerta = alerta_client(
                endpoint=self.alerta_ep,
                key=self.alerta_token)
        else:
            self._display.warning('Alerta python client is not available')

        self.use_last_name_segment = self.get_option('use_last_name_segment')

        self.job_id = os.getenv('TASK_EXECUTOR_JOB_ID')
        self.environment = os.getenv('APIMON_PROFILER_ALERTA_ENV',
                                     'Production')
        self.customer = os.getenv('APIMON_PROFILER_ALERTA_CUSTOMER')
        self.origin = os.getenv('APIMON_PROFILER_ALERTA_ORIGIN')

    def v2_playbook_on_start(self, playbook):
        if not self.playbook_name:
            self.playbook_name = playbook._file_name

    def is_task_interesting(self, task):
        return (
            task.action.startswith('os_')
            or task.action.startswith('otc')
            or task.action.startswith('opentelekomcloud')
            # This is bad, but what else can we do?
            or task.action[:3] in ['rds', 'cce']
            or task.action in ('script', 'command',
                               'wait_for_connection', 'wait_for')
        )

    def v2_playbook_on_task_start(self, task, is_conditional):
        # NOTE(gtema): used attrs might be jinjas, so probably
        # need to update value with the invokation values
        play = task._parent._play
        self._display.vvv('Profiler: task start %s' % (task.dump_attrs()))
        if self.is_task_interesting(task):
            self.current = task._uuid
            if task.action == 'script' and task.get_name() == 'script':
                name = task.args.get('_raw_params')
            else:
                name = task.get_name()
            if self.use_last_name_segment and ':' in name:
                # When we invoke role - it's name is part of the name.
                # Just take the last segment after ':'
                name_parts = name.split(':')
                name = name_parts[-1].strip()
            action = None
            if task.action.startswith('opentelekomcloud'):
                name_parts = task.action.split('.')
                if len(name_parts) > 1:
                    # action is last segment after '.'
                    action = name_parts[-1]
                else:
                    action = task.action
            else:
                action = task.action

            stat_args = {
                'start': time.time_ns(),
                'name': name,
                'long_name': '{play}:{name}'.format(
                    play=play, name=name),
                'action': action,
                'task': task,
                'play': task._parent._play.get_name(),
                'state': task.args.get('state')
            }
            az = task.args.get('availability_zone')
            service = None

            for tag in task.tags:
                # Look for tags on interesting tags
                if 'az=' == tag[:3] and not az:
                    az = tag[3:]
                if tag.startswith('service='):
                    service = tag[8:]

            if not service and action in self.ACTION_SERVICE_MAP:
                service = self.ACTION_SERVICE_MAP[action]
            elif not service:
                # A very nasty fallback
                if action.startswith('wait_for'):
                    service = 'compute'
                # We do not know the action>service mapping. Try to get first
                # part of the name before '_'
                name_parts = action.split('_')
                if len(name_parts) > 1:
                    service = name_parts[0]

            if az:
                stat_args['az'] = to_text(az)
            if service:
                stat_args['service'] = to_text(service)

            self.stats[self.current] = stat_args
            if self._display.verbosity >= 2:
                self.stats[self.current]['path'] = task.get_path()
        else:
            self.current = None

    def _update_task_stats(self, result, rc):
        if self.current is not None:
            duration = time.time_ns() - self.stats[self.current]['start']

            invoked_args = result._result.get('invocation')
            attrs = {
                'changed': result._result['changed'],
                'end': time.time_ns(),
                'duration': duration,
                'rc': rc
            }
            if (isinstance(invoked_args, dict)
                    and 'module_args' in invoked_args):
                module_args = invoked_args.get('module_args')
                if 'availability_zone' in module_args:
                    attrs['az'] = module_args.get('availability_zone')
                if rc == 3:
                    msg = None
                    if 'msg' in result._result:
                        msg = result._result['msg']
                    attrs['raw_response'] = msg
                    attrs['anonymized_response'] = \
                        self._anonymize_message(attrs['raw_response'])
                    attrs['error_category'] = self._get_message_error_category(
                        attrs['anonymized_response'])
            else:
                if rc == 3:
                    msg = None
                    if 'stderr_lines' in result._result:
                        msg = result._result['stderr_lines'][-1]
                    elif 'module_stderr' in result._result:
                        msg = result._result['module_stderr'].splitlines()[-1]
                    attrs['raw_response'] = msg
                    attrs['anonymized_response'] = \
                        self._anonymize_message(attrs['raw_response'])
                    attrs['error_category'] = self._get_message_error_category(
                        attrs['anonymized_response'])

            self.stats[self.current].update(attrs)

            if rc == 3:
                self._send_alert_to_alerta(
                    **self._prepare_alert_data(self.stats[self.current]))

            self.write_metrics_to_influx(self.current, duration, rc)

    def v2_runner_on_skipped(self, result):
        # Task was skipped - remove stats
        self._update_task_stats(result, 1)

    def v2_runner_on_ok(self, result):
        self._display.vvvv('Profiler: result: %s' % result._result)
        self._update_task_stats(result, 0)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self._display.vvvv('Profiler: result: %s' % result._result)
        rc = 3 if not ignore_errors else 2
        self._update_task_stats(result, rc)

    def write_metrics_to_influx(self, task, duration, rc):
        task_data = self.stats[task]
        tags = dict(
            action=task_data['action'],
            play=task_data['play'],
            name=task_data['name'],
            long_name=task_data['long_name'],
            state=task_data['state'],
            result_str=rc_str_struct[rc],
        )
        fields = dict(
            duration=int(duration / 1000000),
            result_code=int(rc)
        )
        if 'az' in task_data:
            tags['az'] = task_data['az']
        if 'service' in task_data:
            tags['service'] = task_data['service']
        if 'raw_response' in task_data:
            fields['raw_response'] = task_data['raw_response']
        if 'anonymized_response' in task_data:
            fields['anonymized_response'] = task_data['anonymized_response']
        if 'error_category' in task_data:
            tags['error_category'] = task_data['error_category']
        if self.environment:
            tags['environment'] = self.environment
        if self.job_id:
            fields['job_id'] = self.job_id
        data = [dict(
            measurement=self.measurement_name,
            tags=tags,
            fields=fields
        )]
        self._write_data_to_influx(data)

    def _write_data_to_influx(self, data):
        try:
            self._display.vv('Stats: %s' % data)
            if self.influxdb_client:
                self.influxdb_client.write_points(data)
        except Exception as e:
            self._display.warning('Profiler: Error writing data to'
                                  'influxdb: %s' % e)
            self._send_alert_to_alerta(
                resource='apimon_profile',
                event='InfluxWriteError',
                value=e.to_str(),
                service=['apimon', 'profiler'],
                severity='major'
            )

    def _prepare_alert_data(self, data):
        link = os.getenv(
            'APIMON_PROFILER_LOG_LINK',
            'https://swift/{job_id}'
        ).format(job_id=self.job_id)
        web_link = '<a href="{}">{}</a>' % (link, self.job_id)

        alert_data = dict(
            environment=self.environment,
            service=['apimon', data.get('service')],
            customer=self.customer,
            resource=data.get('action'),
            event=data.get('error_category',
                           data.get('anonymized_response')),
            # value=data.get('anonymized_response'),
            severity='major',
            value='<a href="{link}">Log</a>'.format(link=link),
            raw_data=data.get('raw_response'),
            attributes={
                'logUrl': link,
                'logUrlWeb': web_link
            }
        )
        if self.customer:
            alert_data['customer'] = self.customer
        if self.origin:
            alert_data['origin'] = self.origin

        self._display.vvv('Alerta data %s' % alert_data)
        return alert_data

    def _send_alert_to_alerta(self, service, resource, event,
                              environment,
                              severity='major',
                              **attrs):
        if not environment:
            environment = self.environment
        if not service:
            service = ['apimon']
        try:
            if self.alerta:
                self.alerta.send_alert(
                    severity=severity,
                    environment=environment,
                    resource=resource,
                    event=event,
                    service=service,
                    **attrs)
        except Exception as e:
            self._display.error(
                 'Profiler: Error sending alert to alerta: %s' % e)

    def _send_heartbeat_to_alerta(self):
        try:
            if self.alerta:
                self.alerta.heartbeat(
                    origin='apimon_callback' + self.environment,
                    tags=['Environment=' + self.environment]
                )
        except Exception as e:
            self._display.error(
                 'Profiler: Error sending Heartbeat to alerta: %s' % e)

    def v2_playbook_on_stats(self, stats):
        global te, t0

        te = time.time_ns()
        self._display.display(tasktime())
        self._display.display(filled("", fchar="="))

        results = self.stats.items()
        overall_apimon_duration = 0
        rcs = {
            0: 0,
            1: 0,
            2: 0,
            3: 0
        }

        # Print the timings
        for uuid, result in results:
            duration = result['duration'] / 1000000
            overall_apimon_duration = overall_apimon_duration + duration
            rcs.update({result['rc']: rcs[result['rc']] + 1})
            msg = u"Action={0}, state={1} duration={2:.02f}, " \
                  u"changed={3}, name={4}".format(
                    result['action'],
                    result['state'],
                    duration/1000,  # MS to Sec
                    result['changed'],
                    result['task'].get_name()
                  )
            self._display.display(msg)

        if self.influxdb_client:
            rescued = 0
            for (host, val) in stats.rescued.items():
                if val:
                    rescued += val
            playbook_rc = 0 if (rcs[3] == 0 and rescued == 0) else 3
            data = [dict(
                measurement=self.measurement_name,
                tags=dict(
                    action='playbook_summary',
                    name=PurePosixPath(self.playbook_name).name,
                    result_str=rc_str_struct[playbook_rc],
                    environment=self.environment
                ),
                fields=dict(
                    duration=int((te-t0)/1000000),
                    apimon_duration=int(overall_apimon_duration),
                    amount_passed=int(rcs[0]),
                    amount_skipped=int(rcs[1]),
                    amount_failed=int(rcs[2]),
                    amount_failed_ignored=int(rcs[3]),
                    result_code=int(playbook_rc),
                    job_id=self.job_id
                )
            )]
            self._write_data_to_influx(data)
        self._send_heartbeat_to_alerta()

        self._display.display(
            'Overall duration of APImon tasks in playbook %s is: %s s' %
            (self.playbook_name, str(overall_apimon_duration / 1000)))

    def _get_message_error_category(self, msg):
        result = None
        # SomeSDKException: 123
        # ResourceNotFound: 404
        exc = re.search(r"(?P<exception>\w*\b):\s(?P<code>\d{3})\b", msg)
        if not exc:
            # (HTTP 404)
            exc = re.search(r"\((?P<exception>\w+) (?P<code>\d{3})\)", msg)
        if exc:
            result = "%s%s" % (exc.group('exception'), exc.group('code'))
            return result

        # contains InternalServerError
        if re.search(r"Internal\s?Server\s?Error", msg):
            result = "HTTP500"
            return result
        # Quota exceeded, quota exceeded, exceeded for quota
        if 'uota ' in msg and ' exceed' in msg:
            result = "QuotaExceeded"
            return result
        # WAF
        if 'The incident ID is:' in msg:
            result = "WAF"
            return result
        if 'ResourceTimeout' in msg:
            return 'ResourceTimeout'

        return result if result else msg

    def _anonymize_message(self, msg):
        # Anonymize remaining part
        # Project_id
        result = msg
        result = re.sub(r"[0-9a-z]{32}", "_omit_", result)
        # UUID
        result = re.sub(r"([0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}"
                        "-[0-9a-z]{4}-[0-9a-z]{12})", "_omit_", result)
        # WAF_ID likes
        result = re.sub(r"[0-9]{5,}", "_omit_", result)
        # Scenario random
        result = re.sub(r"-[0-9a-zA-Z]{12}-", "_omit_", result)
        # tmp12345678
        result = re.sub(r"tmp[0-9a-zA-Z]{8}", "_omit_", result)
        # IP
        result = re.sub(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d*)?",
                        "_omit_", result)

        return result
