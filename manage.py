#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ableton_challenge.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


"""
*       * * * * ( python manage.py send_mail >> ~/cron_mail.log 2>&1)
0,20,40 * * * * (python manage.py retry_deferred >> ~/cron_mail_deferred.log 2>&1)
0 0 * * * (python manage.py purge_mail_log 7 >> ~/cron_mail_purge.log 2>&1)
"""