import subprocess

def export_mysql_db(host, user, password, database, output_file):
    # Construct the mysqldump command
    command = [
        'mysqldump',
        '--host=' + host,
        '--user=' + user,
        '--password=' + password,
        database,
        '--result-file=' + output_file
    ]

    try:
        # Run the mysqldump command
        subprocess.run(command, check=True)
        print(f"Database '{database}' exported successfully to '{output_file}'")
    except subprocess.CalledProcessError as e:
        print(f"Error exporting database '{database}': {e}")

# Example usage
host = "65.0.73.255"
user =  "root"
password =  "django@123"
database = "django_project"
output_file = 'E:\\Manoj Kumar\\DartIn\\GovtProject\\GovtProject\\path_to_save\\exported_database.sql'

export_mysql_db(host, user, password, database, output_file)
#
#     mysql_host =
#     mysql_user =
#     mysql_password =
#     mysql_database =
#
#     # S3 details
#     s3_bucket_name = "s3://mysqldjangoprojectbackup"
#     s3_key = "/path.sql"
#
#     # Export MySQL database
#     export_path = "/home/ec2-user/backup"
#     export_path = "E:\\Manoj Kumar\\DartIn\\GovtProject\\GovtProject\\"
#     exported_file = export_mysql_database(mysql_host, mysql_user, mysql_password, mysql_database, export_path)
#
#     # Upload to S3
#     if exported_file:
#         upload_to_s3(exported_file, s3_bucket_name, s3_key)
