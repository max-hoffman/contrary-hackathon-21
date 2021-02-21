FROM python:3.7

RUN wget \
    https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip \
    -O /usr/lib/chromedriver_linux64.zip \
    && unzip /usr/lib/chromedriver_linux64.zip -d /usr/local/bin
    #&& rm -rf /usr/lib/chromedriver_linux64.zip \
    #&& ln -s /usr/lib/chromedriver /usr/local/bin/

RUN echo $PATH

RUN apt update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1
    #libindicator7 libappindicator1 \
    #chromium-browser

RUN wget \
    #https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    https://www.slimjet.com/chrome/download-chrome.php?file=files%2F83.0.4103.116%2Fgoogle-chrome-stable_current_amd64.deb \
    -O google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /usr/src/

WORKDIR /usr/src

RUN poetry install --no-root

EXPOSE 8000
COPY . /usr/src/
CMD ["uvicorn", "web.app:app", "--forwarded-allow-ips='*'", "--host", "0.0.0.0"]

#USER node

# instead of running npm run start, we use PM2, a production-ready process manager for node js
# PM2 just makes sure our app is always restarted after crashing
