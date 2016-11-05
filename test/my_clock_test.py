# -*- coding: utf-8 -*-
from my_clock import my_clock as pm
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')


def get_time_test1():
    assert(pm.get_time(['1s', '2m', '3h'], []) == 3 * 60 * 60 + 2 * 60 + 1)


def get_time_test2():
    assert(pm.get_time(['100s', '2m', '3h'], []) == 3 * 60 * 60 + 2 * 60 + 100)


def get_time_test3():
    assert(pm.get_time(['100s', '2', '3h'], []) == 3 * 60 * 60 + 2 * 60 + 100)


def get_terminal_escape_test():
    assert(pm.get_terminal_escape("Pomodoro") == "'Pomodoro'")


def get_terminal_escape_test2():
    assert(pm.get_terminal_escape("Pomodoro Job") == "'Pomodoro Job'")


def get_config_options_test():
    conf_filename = os.path.dirname(os.path.abspath(__file__)) + \
        '/confs/clock1.json'
    options = pm.get_config_options(conf_filename)  # use default task
    assert(options == {
        "title": "MyTitle",
        "message": "MyMessage",
        "time": ["3s"]
    })


def get_config_options_test2():
    conf_filename = os.path.dirname(os.path.abspath(__file__)) + \
        '/confs/clock1.json'
    options = pm.get_config_options(conf_filename, task_name='pomodoro-job')
    assert(options == {
        "title": "Pomodoro Job",
        "message": "finished",
        "time": ["25m"]
    })


def get_config_options_test3():
    conf_filename = os.path.dirname(os.path.abspath(__file__)) + \
        '/confs/clock1.json'
    options = pm.get_config_options(conf_filename, task_name=None)
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
        '/confs/clock1.json'
    task_names = pm.get_task_names(conf_filename)
    assert(set(task_names) == {"default", "pomodoro-job", "pomodoro-rest"})

def get_task_names_test():
    conf_filename = os.path.dirname(os.path.abspath(__file__)) + \
        '/confs/empty.json'
    task_names = pm.get_task_names(conf_filename)
    assert(set(task_names) == {"default"})


def merge_options_test1():
    default_options = {
        'message': 'DefaultMessage',
        'title': 'DefaultTitle',
        'show_tasks': False,
        'time': ['2s']}
    conf_options = {
        'message': 'ConfMessage',
        'title': 'ConfTitle',
        'time': ['4s']
    }
    assert(pm.merge_options(default_options, conf_options) == default_options)


def merge_options_test2():
    default_options = {
        'message': '',
        'title': 'DefaultTitle',
        'show_tasks': False,
        'time': []
    }
    conf_options = {
        'message': 'ConfMessage',
        'title': 'ConfTitle',
        'show_tasks': True,
        'time': ['4s']
    }
    assert(pm.merge_options(default_options,
                            conf_options)['show_tasks'] == False)
