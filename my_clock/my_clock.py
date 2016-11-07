#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import sys
import json5
import subprocess
from os import system
import os.path
from time import sleep

__VERSION__ = "0.1.4"

DEFAULT_TITLE = 'MyClock'
DEFAULT_MESSAGE = 'MyClock'
DEFAULT_VERBOSE = False
DEFAULT_CONFIG_JFILENAME = os.path.expanduser('~/.clock.json')
DEFAULT_TASK_NAME = 'default'
DEFAULT_SHOW_TASKS = False
DEFAULT_RING_BELL = False
DEFAULT_BELL_SOUND_FILENAME = os.path.abspath(
    os.path.dirname(os.path.abspath(__file__)) + '/music/default_bell.mp3')


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


def executable_afplay():
    try:
        subprocess.check_output(['which', 'afplay'])
        return True
    except FileNotFoundError:
        return False


def afplay(mp3):
    system('afplay {}'.format(mp3))


class IllegalJson5Error(ValueError):
    """ Illegal Json5 syntax """


def get_config_options(conf_filename=DEFAULT_CONFIG_JFILENAME,
                       task_name=DEFAULT_TASK_NAME):
    """ if task_name is None, return all config_options """
    if not os.path.isfile(conf_filename):
        return {}

    with open(conf_filename) as jf:
        if task_name is None:
            try:
                return json5.load(jf)
            except Exception as ex:
                raise IllegalJson5Error(
                    '{} occurs following json5 syntax error:\n'
                    '{}'.format(conf_filename, ex.args[0]))
        else:
            try:
                return json5.load(jf).get(task_name, {})
            except Exception as ex:
                raise IllegalJson5Error(
                    '{} occurs following json5 syntax error:\n'
                    '{}'.format(conf_filename, ex.args[0]))


def get_task_names(conf_filename=DEFAULT_CONFIG_JFILENAME):
    # if options is set(), return DEFAULT_TASK_NAME
    options = list(get_config_options(conf_filename=conf_filename,
                                      task_name=None))
    if options == []:
        return [DEFAULT_TASK_NAME]
    else:
        return options


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
    # option which takes value
    for key, value in {'message': default_opts['message'],
                       'title': default_opts['title'],
                       'time': default_opts['time']}.items():
        if value:
            options[key] = value
    # store_true option
    for key, value in {'show_tasks': default_opts['show_tasks'],
                       'verbose': default_opts['verbose'],
                       'ring_bell': default_opts['ring_bell']
                       }.items():
        if (key in default_opts and default_opts[key] is True):
            options[key] = value

    options['message'] = options.get('message', DEFAULT_MESSAGE)
    options['title'] = options.get('title', DEFAULT_TITLE)
    options['verbose'] = options.get('verbose', DEFAULT_VERBOSE)
    options['show_tasks'] = options.get('show_tasks', DEFAULT_SHOW_TASKS)
    options['ring_bell'] = options.get('ring_bell', DEFAULT_RING_BELL)
    return options


def get_option_parser():
    usage = 'my_clock [options] times'
    parser = OptionParser(usage=usage, version=__VERSION__)
    parser.add_option(
        '-V', '--verbose',
        action='store_true',
        default=False,
        dest='verbose',
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
        '-r', '--ring-bell',
        action='store_true',
        default=False,
        dest='ring_bell',
        help='verbose'
    )
    parser.add_option(
        '-T', '--task',
        action='store',
        dest='task',
        default=DEFAULT_TASK_NAME,
        type=str,
        help='set task string')
    parser.add_option(
        '-f', '--conf-file',
        action='store',
        dest='conf_filename',
        default=DEFAULT_CONFIG_JFILENAME,
        type=str,
        help='set configure filename string')
    parser.add_option(
        '-l', '--list',
        action='store_true',
        dest='show_tasks',
        default=False,
        help='show task names')
    return parser


def main():
    opts, args = get_option_parser().parse_args()
    conf_filename = opts.conf_filename
    try:
        options = get_config_options(
            conf_filename=conf_filename, task_name=opts.task)
    except IllegalJson5Error as ex:
        sys.stderr.write(ex.args[0] + '\n')
        sys.exit()
    options = merge_options({
        'message': opts.message,
        'title': opts.title,
        'verbose': opts.verbose,
        'show_tasks': opts.show_tasks,
        'ring_bell': opts.ring_bell,
        'time': args
    },
        options)

    if opts.show_tasks:
        for name in get_task_names(conf_filename):
            print(name)
        sys.exit()

    try:
        if 'time' not in options:
            print(options)
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

    if options["verbose"]:
        print('options: {}'.format(str(options)))
        print('sleep {}'.format(sleep_time))
        print('begin {} task'.format(opts.task))
    sleep(sleep_time)
    notify(options['title'], options['message'])

    if options["verbose"]:
        print('finished {} task'.format(opts.task))
    if options['ring_bell']:
        afplay(DEFAULT_BELL_SOUND_FILENAME)


if __name__ == '__main__':
    main()
