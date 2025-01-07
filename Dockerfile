FROM python:3.12-windowsservercore-ltsc2022

WORKDIR /babylab-redcap

RUN pip3 install --upgrade pip

RUN pip3 install flask babylab pywin32 python-dotenv

EXPOSE 5000

CMD ["flask", "--app", "babylab.app", "run", "--host=0.0.0.0", "--port=5000"]
