from distutils.core import setup

setup(
    name='bbdn-rest',
    version='0.0.1',
    packages=['bbdn', 'bbdn.core'],
    url='https://github.com/elmiguel/bbdn-rest',
    license='',
    author='Michael Bechtel',
    author_email='mbechtel@irsc.edu',
    description='A Blackboard REST API CLI Application', requires=['docopt', 'schema']
)
