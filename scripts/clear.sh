#!/bin/bash
. /var/www/venv/bin/activate
for i in `find /var/lib/nginx/cache -type f`; do rm $i ; done
python manage.py invalidate_cachalot
