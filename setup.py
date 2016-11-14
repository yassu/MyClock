from setuptools import setup
from my_clock.my_clock import __VERSION__

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Utilities'
]

setup(
    name='my_clock',
    version=__VERSION__,
    description='my clock',
    long_description=open('README.rst').read(),
    author='Yassu',
    author_email='mathyassu@gmail.com',
    url='https://github.com/yassu/MyClock',
    license='MIT',
    packages=['my_clock'],
    install_requires=['json5'],
    classifiers=classifiers,
    entry_points="""
       [console_scripts]
       my_clock = my_clock.my_clock:main
    """,
)
