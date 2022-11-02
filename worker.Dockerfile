FROM python:3.8-slim

# 
WORKDIR /code

# 
COPY requirements.txt /code/
# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# 
COPY . /code/

CMD ["python", "-m", "app.worker"]