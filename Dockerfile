#FROM python
FROM python:3.9-slim


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /home/ec2-user/GovtProject
COPY requirements.txt .
RUN pip install --upgrade pip

ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev \
        pkg-config \
        cron vim wget s3cmd \
        default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*


COPY crontab /etc/cron.d/crontab
#COPY lockrun /usr/local/bin/lockrun
#RUN chmod 0777 /usr/local/bin/lockrun
RUN #chmod 0644 /etc/cron.d/crontab

RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install gunicorn
COPY . .
# RUN /usr/bin/crontab /etc/cron.d/crontab

RUN touch /var/log/cron.log

#RUN python3 manage.py migrate

RUN python3 manage.py collectstatic

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "GovtProject.wsgi:application"]
