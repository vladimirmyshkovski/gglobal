#!/bin/bash

systemctl restart nginx daphne runworkers redis postgresql
nginx -t