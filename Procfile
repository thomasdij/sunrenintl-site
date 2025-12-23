release: python3 manage.py migrate --noinput && python3 manage.py opensearch document index --force
web: gunicorn sunren_site.wsgi:application --preload --worker-tmp-dir /dev/shm
