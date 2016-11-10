#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import sys
import json5
import subprocess
from os import system
import os.path
import time

__VERSION__ = "0.1.6"

DEFAULT_TITLE = 'MyClock'
DEFAULT_MESSAGE = 'MyClock'
DEFAULT_CONFIG_JFILENAME = os.path.expanduser('~/.clock.json')
DEFAULT_TASK_NAME = 'default'
DEFAULT_BELL_SOUND_FILENAME = os.path.abspath(
    os.path.dirname(os.path.abspath(__file__)) + '/music/default_bell.mp3')


def run_cmd(cmd, options):
    if options['verbose']:
        print('Run command: {}'.format(cmd))
    system(cmd)


def executable_terminal_notifier():
    try:
        subprocess.check_output(['terminal-notifier', '-help'])
        return True
    except FileNotFoundError:
        return False


def get_terminal_escape(s):
    return "'{}'".format(s)


def notify(options):
    run_cmd('terminal-notifier -title {} -message {} -sound default'.format(
        get_terminal_escape(options['title']),
        get_terminal_escape(options['message'])), options)


def executable_afplay():
    try:
        subprocess.check_output(['which', 'afplay'])
        return True
    except subprocess.CalledProcessError:
        return False


def afplay(options):
    run_cmd('afplay {}'.format(DEFAULT_BELL_SOUND_FILENAME), options)


class IllegalJson5Error(ValueError):
    """ Illegal Json5 syntax """

class NotDefinedTaskError(ValueError):
    """ Illegal Json5 syntax """


def spend_time(_time):
    t = _time//60
    for cnt in range(t):
        for j in range(60):
            time.sleep(1)
    for j in range(_time - 60*t):
        time.sleep(1)


def get_option_value(opt_name, default_value, input_opts, conf_opts):
    if input_opts[opt_name] is not None:
        return input_opts[opt_name]
    elif opt_name in conf_opts and conf_opts[opt_name] is not None:
        return conf_opts[opt_name]
    else:
        return default_value


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
                if task_name not in get_task_names(conf_filename=conf_filename):
                    raise NotDefinedTaskError('{} task is not defined.'.format(
                                               task_name))
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
    return {
        'verbose': get_option_value('verbose', False, default_opts, conf_opts),
        'message': get_option_value('message', DEFAULT_MESSAGE, default_opts,
                                    conf_opts),
        'title': get_option_value('title', DEFAULT_TITLE, default_opts,
                                  conf_opts),
        'ring_bell': get_option_value('ring_bell', False, default_opts,
                                      conf_opts),
        'bell_sound': get_option_value('bell_sound', False, default_opts,
                                       conf_opts),
        'hide_popup': get_option_value('hide_popup', False, default_opts,
                                       conf_opts),
        'time': get_option_value('time', [], default_opts, conf_opts)
    }


def get_option_parser():
    usage = 'my_clock [options] times'
    parser = OptionParser(usage=usage, version=__VERSION__)
    # conf opts
    parser.add_option(
        '-V', '--verbose',
        action='store_true',
        dest='verbose',
        help='verbose'
    )
    parser.add_option(
        '-g', '--message',
        action='store',
        dest='message',
        help='set message string')
    parser.add_option(
        '-t', '--title',
        action='store',
        dest='title',
        help='set title string')
    parser.add_option(
        '-r', '--ring-bell',
        action='store_true',
        dest='ring_bell',
        help='ring bell or not'
    )
    parser.add_option(
        '-b', '--bell-sound',
        action='store',
        dest='bell_sound',
        help='mp3 file of bell_sound')
    parser.add_option(
        '--hide-popup',
        action='store_true',
        dest='hide_popup',
        help="don't show popup"
    )

    # not conf opts
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
        'bell_sound': opts.bell_sound,
        'hide_popup': opts.hide_popup,
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

    if options['ring_bell'] and not executable_afplay():
        sys.stderr.write('Please install afplay\n')
        sys.exit()

    if options['hide_popup'] and not options['ring_bell']:
        sys.stderr.write('Please hide_popup is False or ring_bell is True.\n')
        sys.exit()

    if options["verbose"]:
        print('options: {}'.format(str(options)))
        print('sleep {}'.format(sleep_time))
        print('begin {} time'.format(opts.task))
    time.sleep(sleep_time)
    if not options['hide_popup']:
        notify(options)

    if options["verbose"]:
        print('finished {} time'.format(opts.task))
    if options['ring_bell'] and executable_afplay():
        afplay(options)


if __name__ == '__main__':
    # main()
    spend_time(60 * 25)
