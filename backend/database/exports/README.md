# Data Exports

This directory holds data exported from the system. 

When users export case lists, audit logs, or action plans as CSV, JSON, or Excel files, the backend can temporarily generate them in this folder before serving them for download.

## Cleanup

A scheduled task should periodically clean out old export files from this directory to save disk space.
