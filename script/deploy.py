from subprocess import check_output

# test
print('Run nosetests')
check_output(['nosetests'])
print('Run flake8')
check_output(['flake8', 'setup.py',
              'my_clock/my_clock.py', 'test/my_clock_test.py'])

# git tag version
version = check_output(['python', 'my_clock/my_clock.py', '--version'])
version = version.decode('utf-8')[:-1]
check_output(['git', 'tag', version])

# git push
check_output(['git', 'checkout', 'master'])
check_output(['git', 'push'])
check_output(['git', 'checkout', 'develop'])
