#!/bin/bash

nginx -t
systemctl restart nginx daphne runworkers redis postgresql
