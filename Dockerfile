FROM python:3.11

WORKDIR /app


ADD requirements.txt /app/requirements.txt


RUN python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt


RUN apt-get update && apt-get install -y ca-certificates curl gnupg && \
    curl -sLf --retry 3 --tlsv1.2 --proto "=https" 'https://packages.doppler.com/public/cli/gpg.DE2A7741A397C129.key' | gpg --dearmor > /usr/share/keyrings/doppler-cli.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/doppler-cli.gpg] https://packages.doppler.com/public/cli/deb/debian any-version main" | tee /etc/apt/sources.list.d/doppler-cli.list && \
    apt-get update


ADD . /app


ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH


EXPOSE 8000


CMD uvicorn app.main:app --host 0.0.0.0