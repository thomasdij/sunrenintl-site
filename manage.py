#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import subprocess
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sunren_site.settings')
    
    # Run Tailwind watcher in the background
    if 'runserver' in sys.argv:
        subprocess.Popen([
            'tailwindcss',
            '-i', './styles/tailwind.css',
            '-o', './static/css/output.css',
            '--watch'
        ])

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
