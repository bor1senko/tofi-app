FROM jupiterapp/frontend:initial

COPY ./app /frontend/app
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/conf.d/ /etc/nginx/conf.d/

COPY ./nginx/certs/jupiter.cert.pem /etc/ssl/certs/jupiter.cert.pem
COPY ./nginx/certs/jupiter.key.pem /etc/ssl/certs/jupiter.key.pem

WORKDIR /frontend/app
RUN npm install -s

CMD nginx
