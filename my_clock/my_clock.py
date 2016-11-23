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

__VERSION__ = "0.2.2"

DEFAULT_TITLE = 'MyClock'
DEFAULT_MESSAGE = 'MyClock'
DEFAULT_CONFIG_JFILENAME = os.path.expanduser('~/.clock.json')
DEFAULT_TASK_NAME = 'default'
DEFAULT_BGM_SOUND = os.path.abspath(
    os.path.dirname(os.path.abspath(__file__)) + '/music/ticking.wav')
INDENTATION = ' ' * 4


def my_error(msg):
    sys.stderr.write(msg)
    sys.exit()


def run_cmd(cmd, options):
    if options['verbose']:
        print('Run command: {}'.format(cmd))
    system(cmd)


def check_file(filename):
    if filename is None or os.path.isfile(filename):
        return True
    else:
        my_error('{} is not a file.\n'.format(filename))


def executable_growlnotify():
    try:
        subprocess.check_output(['which', 'growlnotify'])
        return True
    except FileNotFoundError:
        return False


def get_terminal_escape(s):
    return "'{}'".format(s)


class PlayThread(threading.Thread):

    def __init__(self, confs):
        super(PlayThread, self).__init__()
        self._confs = confs
        self.play_wav = None

    def kill(self):
        self.play_wav.kill()

    def run(self):
        start_time = time.time()
        now_time = start_time
        self.play_wav = PlayWav(
            {'verbose': False,
             'wav_filename': self._confs['wav_filename'],
             'time': self._confs['time'] - (now_time - start_time)})

        while now_time <= start_time + self._confs['time'] and\
                self.play_wav._killed is False:
            self.play_wav.play()
            now_time = time.time()


def notify(options):
    run_cmd('growlnotify {} -t {} -m {}'.format(
        options['growl_notify_options'],
        get_terminal_escape(options['title']),
        get_terminal_escape(options['message'])), options)


class PlayWav:

    def __init__(self, confs):
        self._confs = confs
        self._killed = False

    @property
    def killed(self):
        return self._killed

    def kill(self):
        self._killed = True

    def play(self):
        import pyaudio
        wf = wave.open(self._confs['wav_filename'], "r")
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
            if 'time' in self._confs and \
                    time.time() - start_time >= self._confs['time']:
                break
            if self._killed:
                break
        stream.close()
        p.terminate()


class IllegalJson5Error(ValueError):
    """ Illegal Json5 syntax """


class NotDefinedTaskError(ValueError):
    """ Illegal Json5 syntax """


def spend_time(_time, out_log=None):
    if not out_log:
        time.sleep(_time)
        return

    for j in tqdm(range(1, _time + 1)):
        time.sleep(1)


def get_option_value(opt_name, default_value, *confs):
    """ assume that opts[0].priority > opts[1].priority > ... """
    for opts in confs:
        if opt_name in opts and opts[opt_name] is not None:
            return opts[opt_name]
    return default_value


def replace_for_config(d):
    d_tmp = dict()
    for key, val in d.items():
        d_tmp[key.replace('-', '_')] = val
    return d_tmp


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
                return replace_for_config(json5.load(jf).get(task_name, {}))
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
            None,
            input_opts, conf_opts, hide_opts),
        'play_bgm': get_option_value(
            'play_bgm', False,
            input_opts, conf_opts, hide_opts),
        'bgm_filename': get_option_value(
            'bgm_filename', None,
            input_opts, conf_opts, hide_opts),
        'growl_notify_options': get_option_value(
            'growl_notify_options',
            '', input_opts, conf_opts, hide_opts),
        'hide_popup': get_option_value('hide_popup', False, input_opts,
                                       conf_opts, hide_opts),
        'force_to_use_task': get_option_value('force_to_use_task',
                                              False,
                                              input_opts,
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
        dest='growl_notify_options',
        help='options of terminal notify')
    parser.add_option(
        '--hide-popup',
        action='store_true',
        dest='hide_popup',
        help="don't show popup"
    )
    parser.add_option(
        '--force-to-use-task',
        action='store_true',
        dest='force_to_use_task',
        help="force to use task"
    )

    # not conf opts
    parser.add_option(
        '-s', '--show',
        action='store_true',
        dest='show',
        default=False,
        help='show options and exit')
    parser.add_option(
        '-T', '--task',
        action='store',
        dest='task',
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
        'growl_notify_options': opts.growl_notify_options,
        'hide_popup': opts.hide_popup,
        'out_log': opts.out_log,
        'force_to_use_task': opts.force_to_use_task,
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
        my_error(ex.args[0] + '\n')
    options = merge_options(input_options, options, hide_options)
    if options['bgm_filename'] is not None:
        options['bgm_filename'] = os.path.expanduser(options['bgm_filename'])
    if options['bell_sound'] is not None:
        options['bell_sound'] = os.path.expanduser(options['bell_sound'])

    if opts.show:
        print('Options:')
        for key, value in options.items():
            print('{} {}: {}'.format(INDENTATION, key, value))
        sys.exit()

    if opts.show_tasks:
        for name in get_task_names(conf_filename):
            print(name)
        sys.exit()

    if options['ring_bell']:
        check_file(options['bell_sound'])
    if options['play_bgm']:
        check_file(options['bgm_filename'])

    if options['force_to_use_task'] and opts.task is None:
        my_error('Force to use option is True and task name is not defined.\n')
    if opts.task is None:
        opts.task = DEFAULT_TASK_NAME

    try:
        if 'time' not in options:
            raise TimeNotFoundError()
        sleep_time = get_time(args, options['time'])
    except TimeNotFoundError:
        my_error('Please input times.\n')
    except TimeSyntaxError as ex:
        my_error(ex.args[0] + '\n')

    if options['play_bgm'] and options['bell_sound'] is None:
        my_error('bell_sound is not defined.\n')

    if options['hide_popup'] and not options['ring_bell']:
        my_error('Please hide_popup is False or ring_bell is True.\n')
    if options["verbose"]:
        print('options: {}'.format(str(options)))
        print('sleep {}'.format(sleep_time))
        print('begin {} time'.format(opts.task))
    try:
        if options['play_bgm']:
            th = PlayThread({'wav_filename': options['bgm_filename'],
                             'time': sleep_time})
            th.start()
        spend_time(sleep_time, out_log=options['out_log'])
        th.kill()

        if not options['hide_popup'] and not executable_growlnotify():
            my_error('Please install terminal_notifier\n')

        if not options['hide_popup']:
            notify(options)

        if options["verbose"]:
            print('finished {} time'.format(opts.task))

        if options['ring_bell']:
            PlayWav({'wav_filename': options['bell_sound']}).play()
    except KeyboardInterrupt:
        print('bye')
        if options['play_bgm']:
            th.kill()
        sys.exit()


if __name__ == '__main__':
    main()
