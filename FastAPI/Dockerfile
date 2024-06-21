# 
FROM python:3.10

WORKDIR /code

ENV SECRET=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ENV PASSWORD=0301c30e3a89fbee0bb2dcc21d8cb948a05ab57e5313c0d19c52bbe3c464d3a32eeffec7dc4c38d58358685c84c248621362f8c6568c683c5079ec69826ee6792f069187a2f5b0a6f7a56d486a018a2d593b
ENV PASSWORDSTR=secret

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]