#!/bin/bash
cd <project directory>
docker-compose run --rm --name certbot certbot bash -c "sleep 6 && certbot certonly --standalone -d xn------dddfnxoenlfghchl4bitc.xn--90ais -d xn--90a0am.xn------dddfnxoenlfghchl4bitc.xn--90ais --test --agree-tos --email narnikgamarnikus@gmail.com --server https://acme-v01.api.letsencrypt.org/directory --rsa-key-size 4096 --verbose --keep-until-expiring --preferred-challenges http-01"
docker exec gglobal_nginx_1 nginx -s reload