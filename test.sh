echo "Run nosetests"
nosetests
echo "Run coverage"
coverage run test/my_clock_test.py
echo "Run flake8"
flake8 setup.py my_clock/my_clock.py test/my_clock_test.py
