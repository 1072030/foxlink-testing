FROM python:3.8-slim

# 
WORKDIR /clean

# 
COPY requirements.txt /clean/
# 
RUN pip install --no-cache-dir --upgrade -r /clean/requirements.txt
# 
COPY . /clean/

RUN sed -i 's/test.json/testLogin_single.json/' /clean/app/env.py
RUN sed -i 's/test1.json/testLogin_single.json/' /clean/app/env.py
RUN sed -i 's/test2.json/testLogin_single.json/' /clean/app/env.py
RUN sed -i 's/test3.json/testLogin_single.json/' /clean/app/env.py
RUN sed -i 's/test4.json/testLogin_single.json/' /clean/app/env.py
RUN sed -i 's/test5.json/testLogin_single.json/' /clean/app/env.py
RUN sed -i 's/test6.json/testLogin_single.json/' /clean/app/env.py
RUN sed -i 's/testLogin.json/testLogin_single.json/' /clean/app/env.py

CMD ["python", "-m", "app.worker"]