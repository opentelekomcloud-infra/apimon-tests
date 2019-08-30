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
import time
import os
import logging

from ansible.module_utils.six.moves import reduce
from ansible.module_utils._text import to_text
from ansible.plugins.callback import CallbackBase

from pathlib import PurePosixPath

try:
    import influxdb
except ImportError:
    influxdb = None


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
    This callback module provides per-task timing, ongoing playbook elapsed
    time and ordered list of top 20 longest running tasks at end.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'os_profiler'
    CALLBACK_NEEDS_WHITELIST = True

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

        if influxdb:
            self.measurement_name = self.get_option('influxdb_measurement')
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

        self.use_last_name_segment = self.get_option('use_last_name_segment')

    def v2_playbook_on_start(self, playbook):
        if not self.playbook_name:
            self.playbook_name = playbook._file_name

    def is_task_interesting(self, task):
        return (
            task.action.startswith('os_') or
            task.action.startswith('otc') or
            task.action in ('script', 'command',
                            'wait_for_connection', 'wait_for'))

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
            stat_args = {
                'start': time.time_ns(),
                'name': name,
                'long_name': '{play}:{name}'.format(
                    play=play, name=name),
                'action': task.action,
                'task': task,
                'play': task._parent._play.get_name(),
                'state': task.args.get('state')
            }
            az = task.args.get('availability_zone')

            for tag in task.tags:
                # Look for tags on interesting tags
                if 'az=' == tag[:3] and not az:
                    # AZ is not available on task, but we want
                    # to bind them
                    az = tag[3:]

            if az:
                stat_args['az'] = to_text(az)

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

            self.stats[self.current].update(attrs)

            self.write_metrics_to_influx(self.current, duration, rc)

    def v2_runner_on_skipped(self, result):
        # Task was skipped - remove stats
        self._update_task_stats(result, 1)

    def v2_runner_on_ok(self, result):
        self._display.vvvv('Profiler: result: %s' % result._result)
        self._update_task_stats(result, 0)

    def v2_runner_on_failed(self, result, ignore_errors=False):
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
            result_str=rc_str_struct[rc]
        )
        fields = dict(
            duration=int(duration / 1000000),
            result_code=int(rc)
        )
        if 'az' in task_data:
            tags['az'] = task_data['az']
        job_id = os.getenv('TASK_EXECUTOR_JOB_ID')
        if job_id:
            fields['job_id'] = job_id
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
                    result_str=rc_str_struct[playbook_rc]
                ),
                fields=dict(
                    duration=int((te-t0)/1000000),
                    apimon_duration=int(overall_apimon_duration),
                    amount_passed=int(rcs[0]),
                    amount_skipped=int(rcs[1]),
                    amount_failed=int(rcs[2]),
                    amount_failed_ignored=int(rcs[3]),
                    result_code=int(playbook_rc),
                    job_id=os.getenv('TASK_EXECUTOR_JOB_ID')
                )
            )]
            self._write_data_to_influx(data)

        self._display.display(
            'Overall duration of APImon tasks in playbook %s is: %s ms' %
            (self.playbook_name, str(overall_apimon_duration)))
