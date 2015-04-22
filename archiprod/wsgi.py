"""
WSGI config for archiprod project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import glob

if os.path.exists('/etc/CRI/archiprod_conf'):
	env_dir = '/etc/CRI/archiprod_conf'
else:
	env_dir = 'envdir'

env_vars = glob.glob(os.path.join(env_dir, '*'))
for env_var in env_vars:
    with open(env_var, 'r') as env_var_file:
        os.environ.setdefault(env_var.split(os.sep)[-1],
                              env_var_file.read().strip())

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
