FROM python:3.11-bullseye

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN mkdir athenian_backend
RUN mkdir story_tracking

COPY athenian_backend/. athenian_backend
COPY story_tracking/. story_tracking
COPY scripts/run_server_docker.sh .
COPY manage.py .

RUN chmod a+x run_server_docker.sh

CMD ./run_server_docker.sh