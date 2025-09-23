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
 - [TEST] First bare run (testing structure and overal project consistency)

 ## Sep-23, 2025
 ### Initial thoughts

 Task class structure should use top-down inheritance to reuse common methods and extend on specifics

 There should be bussiness logic division between scheduler and task manager
 Task manager holds task history and can update tasks
 Task scheduler handles rules and controls only live tasks and upcoming tasks

 ### What happened
 - [UPDATED] Server code and basic configuration
 - [NEW] Task manager class with prototypes
 - [NEW] Task Scheduler class with prototypes
 - [TEST] Simple server start/stop check
 - [TEST] Simple handle call check: '/', '/task', '/scheduler'