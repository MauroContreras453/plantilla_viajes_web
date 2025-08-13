#!/bin/bash
# Script de inicio para Render
pip install -r requirements.txt
gunicorn app:app
