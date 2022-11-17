FROM python:3.8-slim

# 
WORKDIR /autocreate

# 
COPY requirements.txt /autocreate/
# 
RUN pip install --no-cache-dir --upgrade -r /autocreate/requirements.txt
# 
COPY . /autocreate/

CMD ["python", "-m", "app.autocreate"]