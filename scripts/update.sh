git pull
. /var/www/venv/bin/activate
while read LINE; do export $LINE; done < .envvars
pip install -r requirements/production.txt
python manage.py collectstatic 