#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import sys
import json5
import subprocess
from os import system
import os.path
from time import sleep

__VERSION__ = "0.0.5"
# TODO: ファイルを使って Optionを定義できるようにする

DEFAULT_TITLE = 'MyClock'
DEFAULT_MESSAGE = 'MyClock'
DEFAULT_CONFIG_JFILENAME = os.path.expanduser('~/.clock.json')


def executable_terminal_notifier():
    try:
        subprocess.check_output(['terminal-notifier', '-help'])
        return True
    except FileNotFoundError:
        return False


def notify(title, msg):
    system('terminal-notifier -title {} -message {} -sound default'.format(
        title, msg))


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


def get_option_parser():
    usage = 'my_clock [options] times'
    parser = OptionParser(usage=usage, version=__VERSION__)
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
    return parser


def main():
    opts, args = get_option_parser().parse_args()
    options = get_config_options(task_name=opts.task)
    for key, value in {'message': opts.message, 'title': opts.title,
                        'time': args}.items():
        if value:
            options[key] = value
    options['message'] = options.get('message', DEFAULT_MESSAGE)
    options['title'] = options.get('title', DEFAULT_TITLE)

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

    print('sleep {}'.format(sleep_time))
    sleep(sleep_time)
    notify(options['title'], options['message'])

if __name__ == '__main__':
    main()
