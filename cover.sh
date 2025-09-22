#!/bin/bash
PYTHONPATH=. coverage run --source=src ./runtests.py
coverage xml && coverage report