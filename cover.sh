#!/bin/bash
PYTHONPATH=. coverage run --source=trustyscheduler ./runtests.py
coverage xml && coverage report