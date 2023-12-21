#!/bin/bash

## AWS credentials
#export AWS_ACCESS_KEY_ID=your_access_key
#export AWS_SECRET_ACCESS_KEY=your_secret_key
#export AWS_DEFAULT_REGION=your_region
# MySQL credentials
export MYSQL_HOST=52.66.53.122
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=django@123
export MYSQL_DATABASE=django_project

# Backup filename
export BACKUP_FILENAME="backup_$(date +"%Y%m%d%H%M%S").sql"

# Backup MySQL database
mysqldump -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE > /backup/$BACKUP_FILENAME

# Upload backup to S3
aws s3 cp /backup/$BACKUP_FILENAME s3://mysqldjangoprojectbackup/$BACKUP_FILENAME












