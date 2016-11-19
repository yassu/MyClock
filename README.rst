=========
MyClock
=========

*version: 0.2.1*

MyClock is a simple and "programmable" clock program.

.. image:: https://travis-ci.org/yassu/MyClock.svg?branch=master
   :target: https://travis-ci.org/yassu/MyClock
   :alt: Build Status

Usage
=======

.. code::

  my_clock [options] [times]

where `[times]` is a list of syntax of `{num}s`, `{num}m`, `{num}h` or `{num}`.

MyClock program spends 60 * 60 * `h` + 60 * `m` + `s` times and notice by popup
  or music.

How to install
================
.. code::

    % pip install my_clock

or

.. code::

    % python setup.py install

at root directory of this project.

Requirements
==============

- `terminal-notifier <https://rubygems.org/gems/terminal-notifier/>`_

Options
=========

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
======================

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

Verbose option
----------------

*type: bool*
*default: false*

You can define `verbose` option by using configure file.

If value of this options is `true`, this program show all options, running commands and begin / finished task name.

Message Option
----------------

*type: str*
*default: "MyClock"*

You can define `message` option by using configure file.

This value is given for message value of `termina-notify`.

Title Option
----------------

*type: str*
*default: "MyClock"*

You can define `title` option by using configure file.

This value is given for title value of `termina-notify`.

Ring_bell Option
------------------

*type: bool*
*default: false*

You can define `ring_bell` option by using configure file.
If value of this option is `true`, when finishing to spend time, play sound.

Bell_sound Option
-------------------

*type: str*
*default: inner-program sound*

Playing sound when this program is finished.

Play_bgm Option
-----------------

*type: bool*
*default: false*

You can define `ring_bell` option by using configure file.
If value of this option is `true`, while this program spend time, this play music.

Bgm_filename Option
---------------------

*type: str*
*default: inner-program sound*

You can define `bgm_filename` option by using configure file.
Playing sound when this program is speinding time.

Out_log Option
----------------

*type: bool*
*default: false*

You can define `ring_bell` option by using configure file.
When this option is `true`, show progress bar when this program spends time.

Terminal_notify_options Option
--------------------------------

*type: str*
*default: ""*

You can define `terminal-notify-options` option by using configure file.
This value is given for options of `terminal-notify`.

Time Option
-------------

*type: [int, int{s}, int{m}, int{h}]*
*default: []*

You can define `time` option by using configure file.
Each values of this option is working like as stdin.


All Configures
----------------

`verbose`
`message`
`title`
`ring_bell`
`out_log`
`bell_sound`
`play_bgm`
`bgm_filename`
`terminal_notify_options`
`hide_popup`
`time`


LICENSE
=========

MIT
