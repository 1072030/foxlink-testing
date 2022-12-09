FROM python:3.8-slim
# 
WORKDIR /app
#
RUN apt update
#
RUN apt install -y htop
#
RUN apt install -y bmon
# 
RUN apt-get install curl -y
#
RUN apt-get install procps -y
#
# RUN apt-get install iputils-ping
# 
RUN apt-get install ffmpeg libsm6 libxext6 -y
#
RUN apt-get install libmariadb-dev -y
#
RUN apt-get install gcc -y 
# 
COPY requirements.txt /app/
# 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
