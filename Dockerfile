FROM python:3.12-slim

WORKDIR /babylab-redcap

RUN pip3 install --upgrade pip && pip install flask babylab

EXPOSE 5000

CMD ["flask", "run", "--host=127.0.0.1", "--port=5000"]
