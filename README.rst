=========
MyClock
=========

*version: 0.2.5*

MyClock is a simple and "programmable" clock program.

.. image:: https://travis-ci.org/yassu/MyClock.svg?branch=master
   :target: https://travis-ci.org/yassu/MyClock
   :alt: Build Status

Usage
=======

.. code::

  my_clock [options] [times]

where `[times]` is a list of syntax of `{num}s`, `{num}m`, `{num}h` or `{num}`.

MyClock program spends 60 * 60 * `h` + 60 * `m` + `s` times and notice by popup or music.

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

- growlnotify

Options
=========

- `--version`: show program's version number and exit
- `-h`, `--help`: show this help message and exit
- `-V`, `--verbose`: verbose
- `-g MESSAGE`, `--message=MESSAGE`: set message string default: "<sleep_time_min> seconds is spent."
- `-t TITLE`, `--title=TITLE`: set title string. default: "MyClock"
- `-o`, `--log`: out log to stdout
- `-r`, `--ring-bell`: ring bell or not after timer
- `-b BELL_SOUND`, `--bell-sound BELL_SOUND`: mp3 file of bell_sound
- `--bgm`, `--play-bgm`: play bgm
- `--bgm-sound BGM_FILENAME`: bgm music
- `--growl_notify_options GROWL_NOTIFY_OPTIONS`: options of growl notify
- `--hide-popup`: don't show popup
-  `--force-to-use-task`: force to use task
-  `-s, --show`: show options and exit
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

You can embed value of following options in message, title, bgm_filename or bell_sound options as syntax `<{opt_name}>`:

* sleep_time_sec
* sleep_time_min
* sleep_time_hour
* title
* message
* bgm_filename
* bell_sound

Verbose option
----------------

*Corresponding option: -V, --verbose*
*type: bool*
*default: false*

You can define `verbose` option by using configure file.

If value of this options is `true`, this program show all options, running commands and begin / finished task name.

Message Option
----------------

*Corresponding option: -g, --message*
*type: str*
*default: "<sleep_time_sec> seconds is spent."*

You can define `message` option by using configure file.

This value is given for message value of `termina-notify`.

Title Option
----------------

*Corresponding option: -t, --title*
*type: str*
*default: "MyClock"*

You can define `title` option by using configure file.

This value is given for title value of `termina-notify`.

Ring_bell Option
------------------

*Corresponding option: -r, --ring-bell*
*type: bool*
*default: false*

You can define `ring_bell` option by using configure file.
If value of this option is `true`, when finishing to spend time, play sound.

Bell_sound Option
-------------------

*Corresponding option:---bgm-sound*
*type: str*
*default: None*

Playing sound when this program is finished.

Play_bgm Option
-----------------

*Corresponding option:--bgm, play-bgm*
*type: bool*
*default: false*

You can define `ring_bell` option by using configure file.
If value of this option is `true`, while this program spend time, this play music.

Bgm_filename Option
---------------------

*Corresponding option: bgm-sound*
*type: str*
*default: None*

You can define `bgm_filename` option by using configure file.
Playing sound when this program is speinding time.

Out_log Option
----------------

*Corresponding option: -o, --log*
*type: bool*
*default: false*

You can define `ring_bell` option by using configure file.
When this option is `true`, show progress bar when this program spends time.

Growl_notify_options Option
--------------------------------

*Corresponding option: --growl_notify_options*
*type: str*
*default: ""*

You can define `growl_notify_options` option by using configure file.
This value is given for options of `growl-notify`.

Force_to_use_task Option
--------------------------

*Corresponding option: --force-to-use-task*
*type: bool*
*default: false*

You can define `force_to_use_task` option by using configure file.
If this value is True and task name is not defined, raise Error.

Time Option
-------------

*type: [int, int{s}, int{m}, int{h}]*
*default: []*

You can define `time` option by using configure file.
Each values of this option is working like as stdin.


Hide Option
-------------

You can define hide option which like as `_` task. For example,

When this program spent time, hide options is loaded.

Of course, you can "overwrite" usual configure options or stdin.
For example,

::

  {
    "_": {
      "verbose": true,
      "out_log": true,
      "title": "Hide Title",
      "message": "Hide Message"
    },
    "sample": {
    "title": "sample title",
    "message": "sample message",
    "time": ["2s"]
    }
  }



LICENSE
=========

MIT
