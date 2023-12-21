#!/bin/bash

# MySQL Database Information
DB_USER="root"
DB_PASSWORD="django@123"
DB_NAME="django_project"

# S3 Bucket Information
S3_BUCKET="s3://mysqldjangoprojectbackup"
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

# Backup MySQL Database
mysqldump -u$DB_USER -p$DB_PASSWORD $DB_NAME > backup.sql

# Compress the backup
tar -czvf backup_$TIMESTAMP.tar.gz backup.sql

# Upload to S3 Bucket
aws s3 cp backup_$TIMESTAMP.tar.gz $S3_BUCKET/

# Cleanup
rm backup.sql
rm backup_$TIMESTAMP.tar.gz
