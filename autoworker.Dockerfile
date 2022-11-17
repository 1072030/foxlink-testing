FROM python:3.8-slim

# 
WORKDIR /autoworker

# 
COPY requirements.txt /autoworker/
# 
RUN pip install --no-cache-dir --upgrade -r /autoworker/requirements.txt
# 
COPY . /autoworker/

CMD ["python", "-m", "app.autoworker"]