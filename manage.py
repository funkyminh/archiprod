#!/usr/bin/env python
import os
import sys
import glob

from django.conf import settings


if __name__ == "__main__":

    if 'test' == sys.argv[1] :
        env_vars = {
            'DATABASE_ENGINE': 'sqlite3',
            'DATABASE_NAME': 'archiprod',
            'DATABASE_PASSWORD': 'admin',
            'DATABASE_USER': 'root',
            'DEBUG': 'true',
            'DJANGO_SETTINGS_MODULE': 'archiprod.settings',
            'FTP_ROOT': './ftp_test',
            'SECRET_KEY': 'bla',
            'SOLR_ROOT': '/usr/local/Cellar/solr/4.3.0/libexec/example/solr/dev/conf/'
        }
        for key, val in env_vars.items():
            os.environ.setdefault(key , val)
        settings.DATABASES.pop('acanthes', None)
    else:
        if os.path.exists('/etc/CRI/archiprod_conf'):
            env_dir = '/etc/CRI/archiprod_conf'
        else:
            env_dir = 'envdir'
        env_vars = glob.glob(os.path.join(env_dir, '*'))
        for env_var in env_vars:
            with open(env_var, 'r') as env_var_file:
                os.environ.setdefault(env_var.split(os.sep)[-1],
                                      env_var_file.read().strip())

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
