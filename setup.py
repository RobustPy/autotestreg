"""Setup.py for Pypi.org"""
from distutils.core import setup

setup(
    name='autotestreg',
    packages=['autotestreg'],
    version='0.1.1',
    description='Automatically test your functions to see if you have changed their behavior by mistake!',
    author='Nicolas Micaux',

    url='https://github.com/NicolasMICAUX/autotestreg',

    install_requires=[],  # None

    keywords=['test', 'regression', 'automatically'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.5',

    # Set README.md as description
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
