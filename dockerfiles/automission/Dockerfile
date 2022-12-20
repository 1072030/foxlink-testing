FROM python:3.8-slim

# 
WORKDIR /automission
# 
COPY requirements.txt /automission/
#
RUN apt-get update
#
RUN apt-get install libmariadb-dev-compat -y
#
RUN apt-get install gcc -y
#
RUN pip install --no-cache-dir --upgrade -r /automission/requirements.txt
#
COPY . /automission/
#
CMD ["python", "-m", "app.automission"]