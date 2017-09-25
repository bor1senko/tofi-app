FROM jupiterapp/backend:initial

ENV BACKEND_PATH /backend
WORKDIR ${BACKEND_PATH}
COPY . ${BACKEND_PATH}

RUN apt-get update && apt-get -y install cron

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ${BACKEND_PATH}/init/entry.sh