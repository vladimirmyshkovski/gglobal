. /var/www/venv/bin/activate
pip install -r requirements/production.txt
while IFS='' read -r line || [[ -n "$line"  ]]; do
        export $line
        echo exporting $line
done < "$1"
