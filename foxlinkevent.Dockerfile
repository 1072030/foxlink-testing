FROM python:3.8-slim

# 
WORKDIR /foxlinkevent

# 
COPY requirements.txt /foxlinkevent/
# 
RUN pip install --no-cache-dir --upgrade -r /foxlinkevent/requirements.txt
# 
COPY . /foxlinkevent/

CMD ["python", "-m", "app.foxlinkevent"]