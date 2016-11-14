MyClock
=========

*version: 0.2.0*

MyClock is a simple and "programmable" clock program.

.. image:: https://travis-ci.org/yassu/MyClock.svg?branch=master
   :target: https://travis-ci.org/yassu/MyClock
   :alt: Build Status

Usage
-------

.. code::

  my_clock [options] [times]

where `[times]` is a list of syntax of `{num}s`, `{num}m`, `{num}h` or `{num}`.

MyClock program spends 60 * 60 * `h` + 60 * `m` + `s` times and notice by popup.

How to install
----------------
.. code::

    % pip install my_clock

or

.. code::

    % python setup.py install

at root directory of this project.

Requirements
--------------

- `terminal-notifier <https://rubygems.org/gems/terminal-notifier/>`_

Options
---------

- `--version`: show program's version number and exit
- `-h`, `--help`: show this help message and exit
- `-V`, `--verbose`: verbose
- `-g MESSAGE`, `--message=MESSAGE`: set message string default: "MyClock"
- `-t TITLE`, `--title=TITLE`: set title string. default: "MyClock"
- `-o`, `--log`: out log to stdout
- `-r`, `--ring-bell`: ring bell or not after timer
- `-b BELL_SOUND`, `--bell-sound BELL_SOUND`: mp3 file of bell_sound
- `--bgm`, `--play-bgm`: play bgm
- `--bgm-sound BGM_FILENAME`: bgm music
- `--terminal_notify_options TERMINAL_NOTIFY_OPTIONS`: options of terminal notify
- `hide-popup`: don't show popup
- `-T TASK`, `--task=TASK`:  set task string default: "default"
- `-f {filename}`, `--conf-file {filename}`: set configure filename string default: "~/.clock.json"
- `-l`, `--list`: show task names

About Configure File
----------------------

You can define configure in configure file for `json5 <http://json5.org/>`_
format.
Default configure file path is `~/.clock.json`.
You can change configure file path by `--conf-file` option.

For example,

.. code::

  {
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
  }

LICENSE
---------

MIT
