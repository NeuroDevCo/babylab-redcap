
#!/bin/sh
sudo apt-get -y install xdg-utils firefox python3
python3 -m pip install babylab waitress python-dotenv flask

python3 -m flask --app babylab.app run &
xdg-open http://127.0.0.1:5000 &