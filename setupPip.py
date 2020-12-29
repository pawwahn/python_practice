# encoding: utf-8
# *********************************************************************************************************************** setupPip.py.py
"""setupPip.py.py
"""

# ***********************************************************************************************************************

# ======================================================================================================================= Imports
from __future__ import absolute_import
import os
import platform

# ======================================================================================================================= Static

pip = [

    (
        'pytz',
        {
            'ALL': ('pytz', ('2014.4', '2014.7', '2014.9', '2014.10', '2015.7'), None)
        }
    ),

    (
        'python-django',
        {
            'ALL': ('Django', '2.2', None)
        }
    ),
    # todo: Need to purchase for latest version
    # (
    #     'ChartDirector',
    #     {
    #         'ALL': ('ChartDirector-parlant-python', '5.1.1',
    #                 'http://centos.parentlink.net/ECS/ChartDirector-parlant-python.tar.gz')
    #     }
    # ),
    # Not supported by python 3
    # (
    #     'ClientCookie',
    #     {
    #         'ALL': (
    #             'ClientCookie', '1.3.0', 'http://wwwsearch.sourceforge.net/ClientCookie/src/ClientCookie-1.3.0.tar.gz')
    #     }
    # ),
    # todo: Need to point out to latest version
    # (
    #     'LanguageTools-parlant',
    #     {
    #         # 'el7': ('LanguageTools-parlant', ('2.2'),
    #         #         'http://centos.parentlink.net/Uhura/LanguageTools-parlant.tar.gz'),
    #         # 'ALL': ('LanguageTools-parlant', ('2.2'),
    #         #         'http://centos.parentlink.net/Uhura/LanguageTools-parlant.tar.gz')
    #         # todo: We need test this language tool repo and merge to master and make it as installable package
    #         'ALL': ('LanguageTools-parlant', ('2.2.4'),
    #                 'git+https://stash.bbpd.io/scm/parentlink/languagetools-parlant.git@feature/python_upgrade_3.8'
    #                 )
    #     }
    # ),

    (
        'mysqlclient',
        {
            'ALL': ('mysqlclient', '2.0.0', None)
        }
    ),

    (
        'Pillow',
        {
            'el3': ('Pillow', '1.7.8', None),
            'ALL': ('Pillow', ('2.3', '2.4', '2.5', '2.6', '7.2'), None)
        }
    ),

    (
        'PyRSS2Gen',
        {
            'ALL': ('PyRSS2Gen', '1.1', None)
        }
    ),

    (
        'RestrictedPython',
        {
            'ALL': ('RestrictedPython', '5.0', None)
        }
    ),

#    (
#        'bbnagios',
#        {
#            'el7': ('bbnagios', '0.1.0', None)
#        }
#    ),

    (
        'boto3',
        {
            'ALL': ('boto3', '1.4.4', None)
        }
    ),

    (
        'bottlenose',
        {
            'ALL': ('bottlenose', ('0.5', '0.6'), None)
        }
    ),

    (
        'cssmin',
        {
            'ALL': ('cssmin', '0.2.0', None)
        }
    ),

    (
        'cssselect',
        {
            'ALL': ('cssselect', '0.9.1', None)
        }
    ),
    # todo: Need to point out to Django 2.2 compatible version
    # (
    #     'django-piston',
    #     {
    #         # 'el7': ('django-piston3', ('0.3pre2'),
    #         #         'http://centos.parentlink.net/ECS/django-piston3.tar.gz'),
    #         # 'ALL': ('django-piston3', ('0.3pre2'),
    #         #         'http://centos.parentlink.net/ECS/django-piston3.tar.gz')
    #         # todo: We need test this django-piston repo and merge to master and make it as installable package
    #         'ALL': ('django-piston3', ('0.3pre2'),
    #                 'git+https://stash.bbpd.io/scm/parentlink/django-piston3.git'
    #                 )
    #     }
    # ),
    # (
    #     'django-piston',
    #     {
    #         'ALL': ('django-piston3', ('0.3pre1', '0.3pre2', '0.3rc0', '0.3rc1', '0.3rc2'), '--pre django-piston3')
    #     }
    # ),

    (
        'django-cors-headers',
        {
            'ALL': ('django-cors-headers', '2.2.0', None)
        }
    ),

    (
        'factual-api',
        {
            'ALL': ('factual-api', '1.6.0', None)
        }
    ),

    (
        'feedparser',
        {
            'ALL': ('feedparser', '5.1.3', None)
        }
    ),

    (
        'gdata',
        {
            'ALL': ('gdata', '2.0.18', None)
        }
    ),

    (
        'google-api-python-client',
        {
            'ALL': ('google-api-python-client', ('1.10.0',), None)
        }
    ),

    (
        'httplib2',
        {
            'ALL': ('httplib2', '0.18.1', None)
        }
    ),

    (
        'icalendar',
        {
            'ALL': ('icalendar', '3.8', None)
        }
    ),

    (
        'lxml',
        {
            'el3': (None, None, None),
            'ALL': ('lxml', '4.5.1', None)
        }
    ),

    (
        'mechanize',
        {
            'ALL': ('mechanize', '0.4.5', None)
        }
    ),

    (
        'mock',
        {
            'el7': ('mock', '2.0.0', None)
        }
    ),

    (
        'mongoengine',
        {
            'ALL': ('mongoengine', '0.8.7', None)
        }
    ),
    # Not supported
    # (
    #     'mx',
    #     {
    #         'ALL': (
    #             'egenix-mx-base', ('3.2.7', '3.2.8'), 'https://downloads.egenix.com/python/egenix-mx-base-3.2.8.tar.gz')
    #     }
    # ),

    (
        'oauth',
        {
            'ALL': ('oauth', '1.0.1', None)
        }
    ),

    (
        'oauth2client',
        {
            'ALL': ('oauth2client', '3.0', None)
        }
    ),

    (
        'phonenumbers',
        {
            'ALL': ('phonenumbers', '8.12.6', None)
        }
    ),
    # Not used
    # (
    #     'poster',
    #     {
    #         'ALL': ('poster', '0.8.1', None)
    #     }
    # ),
    # todo: Need to work with default xmlrpc
    # (
    #     'py-xmlrpc',
    #     {
    #         'ALL': ('py-xmlrpc', '0.8.8.3', 'http://centos.parentlink.net/ECS/py-xmlrpc.tar.gz')
    #     }
    # ),

    (
        'pymongo',
        {
            'ALL': ('pymongo', ('2.7.2', '2.8'), None)
        }
    ),

    (
        'pyOpenSSL',
        {
            'ALL': (None, None, None),
            'el5': ('pyOpenSSL', '0.12', None),
            'el6': ('pyOpenSSL', '16.1.0', None),
            'el7': ('pyOpenSSL', '17.2.0', None)
        }
    ),

    (
        'python-beautifulsoup',
        {
            'ALL': ('beautifulsoup4', '4.9.1', None)
        }
    ),
    # Not USED
    # (
    #     'python-cloudfiles',
    #     {
    #         'el3': (None, None, None),
    #         'ALL': ('python-cloudfiles', '1.7.11', None)
    #     }
    # ),

    (
        'python-dateutil',
        {
            'ALL': ('python-dateutil', '2.2', None)
        }
    ),
    # Need a alternative
    # (
    #     'python-instagram',
    #     {
    #         'ALL': (
    #             'python-instagram', '1.3.3', 'https://github.com/ParlantTechnology/python-instagram/archive/master.zip')
    #     }
    # ),

    (
        'python-ldap',
        {
            'el3': ('python-ldap', '2.0.1', 'http://centos.parentlink.net/ECS/python-ldap.tar.gz'),
            'el5': ('python-ldap', '2.3.13', None),
            'el6': ('python-ldap', '2.4', None),
            'el7': ('python-ldap', '3.3.1', None)
        }
    ),

    (
        'python-memcached',
        {
            'ALL': ('python-memcached', '1.59', None)
        }
    ),

    (
        'python-paramiko',
        {
            'ALL': ('paramiko', ('1.14', '1.15', '2.7.1'), None)
        }
    ),

    (
        'python-pycurl',
        {
            'ALL': (None, None, None),
            'el5': ('pycurl', '7.15.5', 'http://pycurl.sourceforge.net/download/00-OLD-VERSIONS/pycurl-7.15.5.tar.gz'),
            'el6': ('pycurl', '7.19.3.1', None),
            'el7': ('pycurl', ('7.19.3.1', '7.43.0'), None)
        }
    ),

    (
        'python3-saml',
        {
            'ALL': (None, None, None),
            'el7': ('python3-saml', '1.2.6', None),
        }
    ),

    (
        'python-yaml',
        {
            'ALL': ('PyYAML', ('3.10', '3.11'), None)
        }
    ),

    (
        'qrcode',
        {
            'ALL': ('qrcode', ('4.0', '5.0', '5.1'), None)
        }
    ),

    (
        'reportlab',
        {
            'ALL': ('reportlab', ('3.0', '3.1.44'), None)
        }
    ),

    (
        'requests',
        {
            'ALL': ('requests', ('2.8.0', '2.18.4', '2.11.1', '2.3.0'), None)
        }
    ),

    (
        'requests-ntlm',
        {
            'ALL': ('requests-ntlm', '0.0.3', None)
        }
    ),

    (
        'simplejson',
        {
            'ALL': ('simplejson', ('3.5', '3.6'), None)
        }
    ),

    (
        'sleekxmpp',
        {
            'ALL': ('sleekxmpp', ('1.3.1',), None)
        }
    ),

    (
        'suds-jurko',
        {
            'ALL': ('suds-jurko', '0.6', None)
        }
    ),

    (
        'tweepy',
        {
            'ALL': ('tweepy', '3.9.0', None),
        }
    ),
    (
        'twilio',
        {
            'ALL': ('twilio', '6.44.2', None),
        }
    ),

    (
        'xmlsec',
        {
            'ALL': (None, None, None),
            'el7': ('xmlsec', '1.1.0', None),
        }
    ),

    (
        'uwsgi',
        {
            'el3': (None, None, None),
            'ALL': ('uWSGI', '2.0.19', None)
        }
    ),

    (
        'watchdog',
        {
            'ALL': ('watchdog', '0.8.3', None)
        }

    ),
    (
        'psutil',
        {
            'el7': ('psutil', '5.4.2', None)
        }
    ),
    (
        'cryptography',
        {
            'ALL': (None, None, None),
            'el7': ('cryptography', '3.0', None),  # 2.0 breaks httpserver
        }
    ),
    (
      'pycrypto',
      {
          'ALL': ('pycrypto', '2.6.1', None)
      }
    ),
    (
        'dkimpy',
        {
            'ALL': ('dkimpy', '0.6.2', None),
        }
    ),
    (
        'dnspython',
        {
             'ALL': ('dnspython', '1.15.0', None),
        }
    ),
    (
        'pyinfoblox',
        {
            'ALL': ('pyinfoblox', '0.1.3', None),
        }
    ),
    (
        'tldextract',
        {
            'ALL': ('tldextract', '2.1.0', None),
        }
    ),
    (
        'gitpython',
        {
            'ALL': ('GitPython', '2.1.11', None),
        }
    ),
    (
        'pyasn1',
        {
            'ALL': ('pyasn1', ('0.1.9','0.3.7'), None),
        }
    ),
    (
        'pyasn1-modules',
        {
            'ALL': ('pyasn1-modules', ('0.0.8', '0.2.8'), None),
        }
    ),
    (
        'PyJWT',
        {
            'ALL': ('PyJWT', '1.7.1', None),
        }
    ),
    (
        'ciso8601',
        {
            'ALL': ('ciso8601', '2.1.3', None),
        }
    ),
    (
        'distro',
        {
            'ALL': ('distro', '1.5.0', None),
        }
    ),

]


# ======================================================================================================================= Classes

# ======================================================================================================================= Functions

# --------------------------------------------------------------------------- verify_pip
def verify_pip(dist, install=False):
    if dist == 'el7':
        os.environ['PYCURL_SSL_LIBRARY'] = 'nss'

    freeze = os.popen('pip freeze').read().strip()
    if freeze:
        package_list = list()
        for line in freeze.split('\n'):
            pl = line.strip().split('==', 1)
            if len(pl) == 2:
                package_list.append(pl)
            else:
                pl = line.strip().split(' @ ', 1)
                package_list.append(pl)
        packages = dict(package_list)
        #packages = dict([line.strip().split('==', 1) for line in freeze.split('\n')])
    else:
        packages = []
    pipUninstall = []
    pipInstall = []

    errors = []

    for program, pip_dict in pip:

        if dist in pip_dict:
            name, versions, pip_command = pip_dict[dist]
        elif 'ALL' in pip_dict:
            name, versions, pip_command = pip_dict['ALL']
        else:
            errors.append('%s: Unspported Distribution(pip): %s' % (program, dist))
            return errors

        if type(versions) is str:
            versions = (versions,)

        if name is not None:
            if name not in packages:
                if pip_command:
                    errors.append('%s: Missing third-party pip program: %s' % (program, name))
                    pipInstall.append(pip_command)
                elif versions:
                    errors.append('%s: Missing third-party pip program: %s' % (
                        program, ' or '.join(['%s-%s' % (name, version) for version in versions])))
                    pipInstall.append('%s==%s' % (name, versions[-1]))
                else:
                    errors.append('%s: Missing third-party pip program: %s' % (program, name))
                    pipInstall.append(name)
            elif versions:
                for version in versions:
                    if version in packages[name]:
                        break
                else:
                    errors.append('%s: Incorrect version of third-party pip program: %s (requires: %s)' % (
                        program, packages[name], ' or '.join(versions)))
                    pipUninstall.append(name)
                    if pip_command:
                        pipInstall.append(pip_command)
                    else:
                        pipInstall.append('%s==%s' % (name, versions[-1]))

    if pipUninstall or pipInstall:
        if install:
            if pipUninstall:
                os.system('pip uninstall -y %s' % ' '.join(pipUninstall))
            for pip_install in pipInstall:
                os.system('pip install %s' % pip_install)

        else:
            errors.extend(['', 'Execute:'])
            if pipUninstall:
                errors.append('pip uninstall %s' % ' '.join(pipUninstall))

            if pipInstall:
                errors.extend(['pip install %s' % pip_install for pip_install in pipInstall])

    return errors


# ***********************************************************************************************************************

if __name__ == '__main__':

    # dist = 'el' + platform.dist()[1].split('.')[0]
    dist = platform.release().split('.')[-2]
    verify_pip(dist=dist, install=True)

# ***********************************************************************************************************************
