#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import sys
import threading
import json5
import subprocess
from tqdm import tqdm
from os import system
import os.path
import time
import wave

__VERSION__ = "0.2.1"

DEFAULT_TITLE = 'MyClock'
DEFAULT_MESSAGE = 'MyClock'
DEFAULT_CONFIG_JFILENAME = os.path.expanduser('~/.clock.json')
DEFAULT_TASK_NAME = 'default'
DEFAULT_BELL_SOUND_FILENAME = os.path.abspath(
    os.path.dirname(os.path.abspath(__file__)) + '/music/default_bell.wav')
DEFAULT_BGM_SOUND = os.path.abspath(
    os.path.dirname(os.path.abspath(__file__)) + '/music/ticking.wav')


def run_cmd(cmd, options):
    if options['verbose']:
        print('Run command: {}'.format(cmd))
    system(cmd)


def check_file(filename):
    if filename is None or os.path.isfile(filename):
        return True
    else:
        sys.stderr.write('{} is not a file.\n'.format(filename))
        sys.exit()


def bye_decorator(func):
    import functools

    @functools.wraps(func)
    def wrapper(*args, **kargs):
        try:
            func(*args, **kargs)
        except KeyboardInterrupt:
            print('bye')
            sys.exit()
    return wrapper


def executable_terminal_notifier():
    try:
        subprocess.check_output(['terminal-notifier', '-help'])
        return True
    except FileNotFoundError:
        return False


def get_terminal_escape(s):
    return "'{}'".format(s)


class PlayThread(threading.Thread):

    def __init__(self, confs):
        super(PlayThread, self).__init__()
        self._confs = confs

    def run(self):
        start_time = time.time()
        now_time = start_time

        while now_time <= start_time + self._confs['time']:
            play_wav({
                'verbose': False,
                'wav_filename': self._confs['wav_filename'],
                'time': self._confs['time'] - (now_time - start_time)})
            now_time = time.time()


def notify(options):
    run_cmd('terminal-notifier {} -title {} -message {} -sound default'.format(
        options['terminal_notify_options'],
        get_terminal_escape(options['title']),
        get_terminal_escape(options['message'])), options)


@bye_decorator
def play_wav(confs):
    import pyaudio
    wf = wave.open(confs['wav_filename'], "r")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(1024)
    start_time = time.time()
    while(data != b''):
        stream.write(data)
        data = wf.readframes(1024)
        if 'time' in confs and time.time() - start_time >= confs['time']:
            return
    stream.close()
    p.terminate()


class IllegalJson5Error(ValueError):
    """ Illegal Json5 syntax """


class NotDefinedTaskError(ValueError):
    """ Illegal Json5 syntax """


@bye_decorator
def spend_time(_time, out_log=None):
    if not out_log:
        time.sleep(_time)
        return

    for j in tqdm(range(1, _time + 1)):
        time.sleep(1)


def get_option_value(opt_name, default_value,
                     input_opts, conf_opts, hide_opts={}):
    if input_opts[opt_name] is not None:
        return input_opts[opt_name]
    elif opt_name in conf_opts and conf_opts[opt_name] is not None:
        return conf_opts[opt_name]
    elif opt_name in hide_opts and hide_opts[opt_name] is not None:
        return hide_opts[opt_name]
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
                if task_name not in \
                        get_task_names(conf_filename=conf_filename):
                    raise NotDefinedTaskError('{} task is not defined.'.format(
                        task_name))
                return json5.load(jf).get(task_name, {})
            except Exception as ex:
                raise IllegalJson5Error(
                    '{} occurs following json5 syntax error:\n'
                    '{}'.format(conf_filename, ex.args[0]))


def get_task_names(conf_filename=DEFAULT_CONFIG_JFILENAME):
    # if options is set(), return DEFAULT_TASK_NAME
    option_names = sorted(list(get_config_options(conf_filename=conf_filename,
                                                  task_name=None)))
    if DEFAULT_TASK_NAME not in option_names:
        option_names.insert(0, DEFAULT_TASK_NAME)
    if option_names == []:
        return [DEFAULT_TASK_NAME]
    else:
        return option_names


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


def merge_options(input_opts, conf_opts, hide_opts):
    return {
        'verbose': get_option_value('verbose', False,
                                    input_opts, conf_opts, hide_opts),
        'message': get_option_value('message', DEFAULT_MESSAGE,
                                    input_opts, conf_opts, hide_opts),
        'title': get_option_value('title', DEFAULT_TITLE,
                                  input_opts, conf_opts, hide_opts),
        'ring_bell': get_option_value('ring_bell', False,
                                      input_opts, conf_opts, hide_opts),
        'out_log': get_option_value('out_log', False,
                                    input_opts, conf_opts, hide_opts),
        'bell_sound': get_option_value(
            'bell_sound',
            DEFAULT_BELL_SOUND_FILENAME,
            input_opts, conf_opts, hide_opts),
        'play_bgm': get_option_value(
            'play_bgm', False,
            input_opts, conf_opts, hide_opts),
        'bgm_filename': get_option_value(
            'bgm_filename', DEFAULT_BGM_SOUND,
            input_opts, conf_opts, hide_opts),
        'terminal_notify_options': get_option_value(
            'terminal_notify_options',
            '', input_opts, conf_opts, hide_opts),
        'hide_popup': get_option_value('hide_popup', False, input_opts,
                                       conf_opts, hide_opts),
        'time': get_option_value('time', [], input_opts, conf_opts, hide_opts)
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
        '--log', '-o',
        action='store_true',
        dest='out_log',
        help='out log to stdout')
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
        '--bgm', '--play-bgm',
        action='store_true',
        dest='play_bgm',
        help='play bgm sound')
    parser.add_option(
        '--bgm-sound',
        action='store',
        dest='bgm_filename',
        help='bgm filename')
    parser.add_option(
        '--terminal-notify-options',
        action='store',
        dest='terminal_notify_options',
        help='options of terminal notify')
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
        # このoptionのdefault値は, このファイルが存在せず, optionsを指定しない
        # 場合にエラーにならないようにするため後で定義する
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
    input_options = {
        'message': opts.message,
        'title': opts.title,
        'verbose': opts.verbose,
        'show_tasks': opts.show_tasks,
        'ring_bell': opts.ring_bell,
        'bell_sound': opts.bell_sound,
        'play_bgm': opts.play_bgm,
        'bgm_filename': opts.bgm_filename,
        'terminal_notify_options': opts.terminal_notify_options,
        'hide_popup': opts.hide_popup,
        'out_log': opts.out_log,
        'time': args if len(args) > 0 else None
    }

    check_file(opts.conf_filename)
    conf_filename = DEFAULT_CONFIG_JFILENAME if opts.conf_filename is None\
        else(opts.conf_filename)

    try:
        options = get_config_options(
            conf_filename=conf_filename, task_name=opts.task)
        if "_" in get_task_names(conf_filename=conf_filename):
            hide_options = get_config_options(
                conf_filename=conf_filename, task_name='_')
        else:
            hide_options = {}
    except IllegalJson5Error as ex:
        sys.stderr.write(ex.args[0] + '\n')
        sys.exit()
    options = merge_options(input_options, options, hide_options)

    check_file(options['bell_sound'])
    check_file(options['bgm_filename'])

    if opts.show_tasks:
        for name in get_task_names(conf_filename):
            print(name)
        sys.exit()

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

    if options['hide_popup'] and not options['ring_bell']:
        sys.stderr.write('Please hide_popup is False or ring_bell is True.\n')
        sys.exit()
    if options['play_bgm']:
        th = PlayThread({'wav_filename': options['bgm_filename'],
                         'time': sleep_time})
        th.start()
    if options["verbose"]:
        print('options: {}'.format(str(options)))
        print('sleep {}'.format(sleep_time))
        print('begin {} time'.format(opts.task))
    spend_time(sleep_time, out_log=options['out_log'])

    if not options['hide_popup']:
        notify(options)

    if options["verbose"]:
        print('finished {} time'.format(opts.task))

    if options['ring_bell']:
        play_wav({'wav_filename': DEFAULT_BELL_SOUND_FILENAME})


if __name__ == '__main__':
    main()
