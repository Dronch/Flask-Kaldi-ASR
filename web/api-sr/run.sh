#!/bin/bash

echo "Runing gunicorn app"
gunicorn --name app -b 0.0.0.0:8000 --reload app:app
