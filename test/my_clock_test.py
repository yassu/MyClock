# -*- coding: utf-8 -*-
from my_clock import my_clock as cl
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')


def get_time_test1():
    assert(cl.get_time(['1s', '2m', '3h'], []) == 3 * 60 * 60 + 2 * 60 + 1)


def get_time_test2():
    assert(cl.get_time(['100s', '2m', '3h'], []) == 3 * 60 * 60 + 2 * 60 + 100)


def get_time_test3():
    assert(cl.get_time(['100s', '2', '3h'], []) == 3 * 60 * 60 + 2 * 60 + 100)


def get_terminal_escape_test():
    assert(cl.get_terminal_escape("Pomodoro") == "'Pomodoro'")


def get_terminal_escape_test2():
    assert(cl.get_terminal_escape("Pomodoro Job") == "'Pomodoro Job'")


def get_config_options_test():
    conf_filename = os.path.dirname(os.path.abspath(__file__)) + \
        '/confs/clock1.json5'
    options = cl.get_config_options(conf_filename)  # use default task
    assert(options == {
        "title": "MyTitle",
        "message": "MyMessage",
        "time": ["3s"]
    })


def get_config_options_test2():
    conf_filename = os.path.dirname(os.path.abspath(__file__)) + \
        '/confs/clock1.json5'
    options = cl.get_config_options(conf_filename, task_name='pomodoro-job')
    assert(options == {
        "title": "Pomodoro Job",
        "message": "finished",
        "time": ["25m"]
    })


def get_config_options_test3():
    conf_filename = os.path.dirname(os.path.abspath(__file__)) + \
        '/confs/clock1.json5'
    options = cl.get_config_options(conf_filename, task_name=None)
    assert(options == {
        "default": {
            "title": "MyTitle",
            "message": "MyMessage",
            "time": ["3s"]
        },
        "pomodoro-job": {
            "title": "Pomodoro Job",
            "message": "finished",
            "time": ["25m"]
        },
        "pomodoro-rest": {
            "title": "Pomodoro Rest",
            "message": "Rest is finished",
            "time": ["5m"]
        }
    })


def get_task_names_test():
    conf_filename = os.path.dirname(os.path.abspath(__file__)) + \
        '/confs/clock1.json5'
    task_names = cl.get_task_names(conf_filename)
    assert(set(task_names) == {"default", "pomodoro-job", "pomodoro-rest"})


def get_task_names_test2():
    conf_filename = os.path.dirname(os.path.abspath(__file__)) + \
        '/confs/empty.json5'
    task_names = cl.get_task_names(conf_filename)
    assert(set(task_names) == {"default"})


def merge_options_test1():
    default_options = {
        'message': 'DefaultMessage',
        'title': 'DefaultTitle',
        'show_tasks': False,
        'verbose': False,
        'time': ['2s']}
    conf_options = {
        'message': 'ConfMessage',
        'title': 'ConfTitle',
        'time': ['4s']
    }
    print(cl.merge_options(default_options, conf_options))
    assert cl.merge_options(default_options, conf_options) == default_options,\
        '{} != {}'.format(cl.merge_options(default_options, conf_options),
                          default_options)


def merge_options_test2():
    default_options = {
        'message': '',
        'title': 'DefaultTitle',
        'show_tasks': False,
        'verbose': False,
        'time': []
    }
    conf_options = {
        'message': 'ConfMessage',
        'title': 'ConfTitle',
        'verbose': True,
        'show_tasks': True,
        'time': ['4s']
    }
    assert(cl.merge_options(default_options,
                            conf_options)['show_tasks'] is False)


def merge_options_test3():
    default_options = {
        'message': '',
        'title': 'DefaultTitle',
        'show_tasks': False,
        'verbose': False,
        'time': []
    }
    conf_options = {
        'message': 'ConfMessage',
        'title': 'ConfTitle',
        'verbose': True,
        'show_tasks': True,
        'time': ['4s']
    }
    assert(cl.merge_options(default_options,
                            conf_options)['verbose'] is False)
