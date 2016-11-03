from setuptools import setup

__VERSION__ = '0.0.3'

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Utilities',
]

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Unix',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Terminals'
]

setup(
    name='my_clock',
    version=__VERSION__,
    description='my clock',
    long_description=open('README.rst').read(),
    author='Yassu',
    author_email='mathyassu@gmail.com',
    url='https://github.com/yassu/MyClock',
    packages=['my_clock'],
    classifiers=classifiers,
    entry_points="""
       [console_scripts]
       my_clock = my_clock.my_clock:main
    """,
)
