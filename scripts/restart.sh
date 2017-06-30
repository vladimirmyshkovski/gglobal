#!/bin/bash

nginx -t
systemctl restart nginx daphne runworkers redis postgresql
systemctl status nginx daphne runworkers redis postgresql