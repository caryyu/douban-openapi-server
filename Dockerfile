FROM python:3.9.4-buster

# Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install google-chrome-unstable \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Chrome webdriver
RUN CHROME_DRIVER_REMOTEPATH=$(wget -q -O - https://chromedriver.storage.googleapis.com | grep -oP '(?<=Key>)[^<]*' | grep chromedriver_linux64.zip | sort -Vr | head -1 ) \
  && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_REMOTEPATH \
  && rm -rf /opt/selenium/chromedriver \
  && unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
  && rm /tmp/chromedriver_linux64.zip \
  && mv /opt/selenium/chromedriver /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
  && chmod 755 /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
  && ln -fs /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION /usr/bin/chromedriver

# Flask Server Setup
ADD . /app
WORKDIR /app

RUN pip install pipenv
RUN pipenv install 

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=0
ENTRYPOINT ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]

