MyClock
=========

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
- `-g MESSAGE`, `--message=MESSAGE`: set message string default: "MyClock"
- `-t TITLE`, `--title=TITLE`: set title string. default: "MyClock"
- `-T TASK`, `--task=TASK`:  set task string default: "default"
- `-V`, `--verbose`: verbose
- `-f {filename}`, `--conf-file`: set configure filename string default: "~/.clock.json"

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
