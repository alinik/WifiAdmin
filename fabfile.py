from contextlib import contextmanager

import os
from fabric.context_managers import prefix
from fabric.contrib.project import rsync_project
from fabric.operations import local, put, sudo
from fabric.state import env

PROJECT_NAME = 'wifinder'
PROJECT_ROOT = '/opt/%s' % PROJECT_NAME
VENV_DIR = os.path.join(PROJECT_ROOT, 'venv')


env.user = 'deploy'
env.hosts = ['map']
env.key_filename = ['contrib/deploy_key.pem']
env.host_key = '|1|Uil+jdG51sfTD63719Gjh0DrAuY=|TVIqk1eVt+943ojN9bf9XWJrmh0= ecdsa-sha2-nistp256 AAAAE2VjZHNh' \
               'LXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBHikOHuQRHjvAQPUdtuB/ioHnBLjPJUn1E0gzhhU3TBGb8KQMl94X' \
               'y2Qc9vLg5+UQflNTaAdCOAd1t3APYs3ugQ='


def add_host():
    test = env.host_key.split('|')[2]
    local('''grep -q {} ~/.ssh/known_hosts ||echo '{}' >> ~/.ssh/known_hosts'''.format(test, env.host_key))


def deploy():
    rsync_project(remote_dir='/var/www/html/', local_dir='src/')


def data():
    local('python contrib/extract.py')
    put('src/js/data.js', '/var/www/html/js/data.js')


@contextmanager
def virtualenv():
    with prefix("source %s" % os.path.join(VENV_DIR,'bin/activate')):
        yield


def chown():
    """Sets proper permissions"""
    sudo('chown -R www-data:www-data %s' % PROJECT_ROOT)
