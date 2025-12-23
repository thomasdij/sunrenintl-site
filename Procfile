release: python manage.py migrate && echo "y" | python manage.py opensearch document index
web: gunicorn sunren_site.wsgi:application --preload --worker-tmp-dir /dev/shm
