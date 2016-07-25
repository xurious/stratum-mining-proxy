#!/usr/bin/env python

from setuptools import setup
import sys, os
try:
    import py2exe
except ImportError:
    py2exe = None

from mining_libs import version

args = {
    'name': 'stratum_mining_proxy',
    'version': version.VERSION,
    'description': 'HTTP-compatible proxy for Sia Stratum mining pools',
    'author': 'SiaMining',
    'author_email': 'dev@siamining.com',
    'url': 'http://siamining.com/stratum',
    'py_modules': ['mining_libs.client_service', 'mining_libs.getwork_listener',
                   'mining_libs.jobs',
                   'mining_libs.multicast_responder', 'mining_libs.stratum_listener',
                   'mining_libs.utils', 'mining_libs.version', 'mining_libs.worker_registry'],
    'install_requires': ['setuptools>=0.6c11', 'twisted>=12.2.0', 'autobahn', 'ecdsa', 'argparse', 'pyblake2'],
    'scripts': ['mining_proxy.py'],
}

if py2exe != None:
    args.update({
        # py2exe options
        'options': {'py2exe':
                      {'optimize': 2,
                       'bundle_files': 1,
                       'compressed': True,
                       'dll_excludes': ['mswsock.dll', 'powrprof.dll'],
                      },
                  },
        'console': ['mining_proxy.py'],
        'zipfile': None,
    })

setup(**args)
