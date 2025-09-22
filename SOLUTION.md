# Chronological

## Sep-22, 2025 (0.5h)

### Initial thoughts

To speed things up, task would be saved as YAMLs in a data folder with interface class, so it could be updated to DB interface later on, if needed

Internal scheduler use should be considered

As a webserver, falcon should be used as more lightweight and simple comparing to monster packaged flask

Tasks should be isolated Python modules with externally configured parameters

Task modules should be managed by scheduler class that implements mentioned execution rules

### What happened

 - [NEW] Package structure, profiling scripts, test base
 - [NEW] setup.py
 - [NEW] First bare run