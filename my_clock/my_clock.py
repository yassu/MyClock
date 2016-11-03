from optparse import OptionParser
import sys
import subprocess
from os import system
from time import sleep

__VERSION__ = "0.0.4"
# TODO: ファイルを使って Optionを定義できるようにする

DEFAULT_SPEND_TIME = 25 * 60
# DEFAULT_SPEND_TIME = 3
DEFAULT_TITLE = 'MyClock'
DEFAULT_MESSAGE = 'MyClock'

def executable_terminal_notifier():
    try:
        subprocess.check_output(['terminal-notifier', '-help'])
        return True
    except FileNotFoundError:
        return False

def notify(title, msg):
    system('terminal-notifier -title {} -message {} -sound default'.format(
        title, msg))

class TimeSyntaxError(ValueError):
    """ Time Syntax Error """

class TimeNotFoundError(ValueError):
    """ TimeNotFoundError """

def get_time(times):
    if len(times) == 0:
        raise TimeNotFoundError('TIME IS NOT FOUND')

    _time = 0
    for t in times:
        if len(t) >= 1 and t[:-1].isdigit() and t[-1] == 'h': # hour
            _time += 60 * 60 * int(t[:-1])
        elif len(t) >= 1 and t[:-1].isdigit() and t[-1] == 'm': # minute
            _time += 60 * int(t[:-1])
        elif len(t) >= 1 and t[:-1].isdigit() and t[-1] == 's': # second
            _time += int(t[:-1])
        elif len(t) >= 1 and t.isdigit():   # minute
            _time += 60 * int(t)
        else:
            raise TimeSyntaxError('{} is illegal as time.'.format(t))
    else:
        return _time


def get_option_parser():
    usage = 'my_clock [options] times'
    parser = OptionParser(usage=usage, version=__VERSION__)
    parser.add_option(
        '-g', '--message',
        action='store',
        dest='message',
        type=str,
        default=DEFAULT_MESSAGE,
        help='set message string')
    parser.add_option(
        '-t', '--title',
        action='store',
        dest='title',
        type=str,
        default=DEFAULT_TITLE,
        help='set title string')
    return parser

def main():
    opts, args = get_option_parser().parse_args()

    try:
        sleep_time = get_time(args)
    except TimeNotFoundError:
        sys.stderr.write('Please input times.\n')
        sys.exit()
    except TimeSyntaxError as ex:
        sys.stderr.write(ex.args[0] + '\n')
        sys.exit()

    if not executable_terminal_notifier():
        std.stderr.write('Please install terminal_notifier\n')

    print('sleep {}'.format(sleep_time))

    sleep(sleep_time)
    notify(opts.title, opts.message)

if __name__ == '__main__':
    main()
