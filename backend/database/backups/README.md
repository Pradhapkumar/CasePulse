# Database Backups

This directory is intended for storing automated or manual database backups.

If using SQLite, you can simply copy the `casepulse.db` file here periodically.

If using PostgreSQL, you can use `pg_dump` and store the `.sql` or `.dump` files in this directory.

## Automated Backups (Future)

A cron job or Celery task can be set up to automatically dump the database into this directory every night, appending a timestamp to the filename (e.g., `backup_2023-10-27.sql`).
