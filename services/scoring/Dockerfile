FROM jupiterapp/backend:initial

ENV SCORING_PATH /scoring
WORKDIR ${SCORING_PATH}
COPY . ${SCORING_PATH}

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ${SCORING_PATH}/app.py