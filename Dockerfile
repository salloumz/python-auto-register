FROM selenium/standalone-chrome

WORKDIR /app
COPY . .

USER root
RUN apt-get update
RUN apt-get install python3-distutils -y
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install selenium
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "main.py"]