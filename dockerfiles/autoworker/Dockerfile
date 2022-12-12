FROM python:3.8-slim

# 
WORKDIR /autoworker
# 
COPY requirements.txt /autoworker/
#
RUN apt-get update
#
RUN apt-get install libmariadb-dev-compat -y
#
RUN apt-get install gcc -y
#
RUN pip install --no-cache-dir --upgrade -r /autoworker/requirements.txt
#
COPY . /autoworker/
#
CMD ["python", "-m", "app.autoworker"]