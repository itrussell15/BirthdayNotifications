FROM ubuntu:latest

#Set environment variable
ENV INSIDE_DOCKER Yes

# Install cron
RUN apt-get update
RUN apt-get install cron

RUN mkdir /home/schmuck

RUN apt-get install nano -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

ADD requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/birthday-notifications

# Add shell script and grant execution rights
ADD script.sh /script.sh
RUN chmod +x /script.sh

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/birthday-notifications

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
