#!/bin/bash

for i in `find /var/lib/nginx/cache -type f`; do rm $i ; done
python manage.py invalidate_cachalot