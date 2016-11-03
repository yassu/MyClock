MyClock
=========

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

- terminal-notifier

Options
---------

- `--version`: show program's version number and exit
- `-h`, `--help`: show this help message and exit
- `-g MESSAGE`, `--message=MESSAGE`: set message string
- `-t TITLE`, `--title=TITLE`: set title string


LICENSE
---------

MIT
