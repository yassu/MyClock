from setuptools import setup

__VERSION__ = '0.0.3'

setup(
    name='my_clock',
    version=__VERSION__,
    description='my clock',
    # long_description=open('README.rst').read(),
    author='Yassu',
    author_email='mathyassu@gmail.com',
    # url='https://github.com/yassu/hyuki-cvs-graph',
    packages=['my_clock'],
    # classifiers=classifiers,
    entry_points="""
       [console_scripts]
       my_clock = my_clock.my_clock:main
    """,
)

