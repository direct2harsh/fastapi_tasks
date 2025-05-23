FROM python:3.13-slim

WORKDIR /app

EXPOSE 3216

COPY . ./

RUN pip install --upgrade setuptools wheel 

RUN pip install -r requirements.txt

CMD [ "python" ,"main.py" ]