FROM python:3.10

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./stock /code/stock
COPY ./base /code/base

#
CMD ["uvicorn", "stock.main:app", "--host", "0.0.0.0", "--port", "8081"]