#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import sys
import json5
import subprocess
from os import system
import os.path
from time import sleep

__VERSION__ = "0.1.3"

DEFAULT_TITLE = 'MyClock'
DEFAULT_MESSAGE = 'MyClock'
DEFAULT_CONFIG_JFILENAME = os.path.expanduser('~/.clock.json')


def executable_terminal_notifier():
    try:
        subprocess.check_output(['terminal-notifier', '-help'])
        return True
    except FileNotFoundError:
        return False


def get_terminal_escape(s):
    return "'{}'".format(s)


def notify(title, msg):
    system('terminal-notifier -title {} -message {} -sound default'.format(
        get_terminal_escape(title), get_terminal_escape(msg)))


def get_config_options(conf_filename=DEFAULT_CONFIG_JFILENAME,
                       task_name='default'):
    if not os.path.isfile(conf_filename):
        return {}

    with open(conf_filename) as jf:
        return json5.load(jf).get(task_name, {})


class TimeSyntaxError(ValueError):
    """ Time Syntax Error """


class TimeNotFoundError(ValueError):
    """ TimeNotFoundError """


def get_time(times, conf_times):
    if len(times) == 0 and len(conf_times) == 0:
        raise TimeNotFoundError('TIME IS NOT FOUND')
    if len(times) == 0:
        times = conf_times

    _time = 0
    for t in times:
        if len(t) >= 1 and t[:-1].isdigit() and t[-1] == 'h':  # hour
            _time += 60 * 60 * int(t[:-1])
        elif len(t) >= 1 and t[:-1].isdigit() and t[-1] == 'm':  # minute
            _time += 60 * int(t[:-1])
        elif len(t) >= 1 and t[:-1].isdigit() and t[-1] == 's':  # second
            _time += int(t[:-1])
        elif len(t) >= 1 and t.isdigit():   # minute
            _time += 60 * int(t)
        else:
            raise TimeSyntaxError('{} is illegal as time.'.format(t))
    else:
        return _time


def merge_options(default_opts, conf_opts):
    options = conf_opts.copy()
    for key, value in {'message': default_opts['message'],
                       'title': default_opts['title'],
                       'time': default_opts['time']}.items():
        if value:
            options[key] = value
    options['message'] = options.get('message', DEFAULT_MESSAGE)
    options['title'] = options.get('title', DEFAULT_TITLE)
    return options


def get_option_parser():
    usage = 'my_clock [options] times'
    parser = OptionParser(usage=usage, version=__VERSION__)
    parser.add_option(
        '-V', '--verbose',
        action='store_true',
        default=False,
        dest='is_verbose',
        help='verbose'
    )
    parser.add_option(
        '-g', '--message',
        action='store',
        dest='message',
        type=str,
        help='set message string')
    parser.add_option(
        '-t', '--title',
        action='store',
        dest='title',
        type=str,
        help='set title string')
    parser.add_option(
        '-T', '--task',
        action='store',
        dest='task',
        default='default',
        type=str,
        help='set task string')
    parser.add_option(
        '-f', '--conf-file',
        action='store',
        dest='conf_filename',
        default=DEFAULT_CONFIG_JFILENAME,
        type=str,
        help='set configure filename string')
    return parser


def main():
    opts, args = get_option_parser().parse_args()
    conf_filename = opts.conf_filename
    options = get_config_options(
        conf_filename=conf_filename, task_name=opts.task)
    options = merge_options({
        'message': opts.message,
        'title': opts.title,
        'time': args
    },
        options)

    try:
        if 'time' not in options:
            raise TimeNotFoundError()
        sleep_time = get_time(args, options['time'])
    except TimeNotFoundError:
        sys.stderr.write('Please input times.\n')
        sys.exit()
    except TimeSyntaxError as ex:
        sys.stderr.write(ex.args[0] + '\n')
        sys.exit()

    if not executable_terminal_notifier():
        sys.stderr.write('Please install terminal_notifier\n')
        sys.exit()

    if opts.is_verbose:
        print('options: {}'.format(str(options)))
        print('sleep {}'.format(sleep_time))
        print('begin {} task'.format(opts.task))
    sleep(sleep_time)
    notify(options['title'], options['message'])

    if opts.is_verbose:
        print('finished {} task'.format(opts.task))

if __name__ == '__main__':
    main()
