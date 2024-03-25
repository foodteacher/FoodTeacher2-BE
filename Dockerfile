FROM python:3.12
ENV MYSQL_HOST=10.106.159.154
ENV MYSQL_PORT=3306
ENV MYSQL_ROOT_PASSWORD=foodteacher123
ENV MYSQL_DATABASE=foodteacher_v2
ENV MYSQL_USER=user1
ENV MYSQL_PASSWORD=foodteacher123
ENV OPENAI_API_KEY=""
ENV SECRET_KEY=15f97448a575823e97d4e8718df130811ef9af4fe1ac6b29bea1f122b1b63ecf

ENV KAKAO_REST_API_KEY=536cb646ce60d71102dc92d2b7845c8d
ENV NAVER_CLIENT_ID=qU9_oHtNaqwsFaPvaS3B
ENV NAVER_SECRET=TGyQd9ReNW

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./FT_api /code/FT_api

#
COPY ./server.py /code/server.py

# 
CMD python /code/server.py