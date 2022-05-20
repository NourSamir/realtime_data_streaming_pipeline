FROM python:3.7

LABEL org.opencontainers.image.authors="noursamir96@gmail.com"
MAINTAINER Nour Samir

WORKDIR /app
COPY . /app

ENV PYTHONPATH=${PYTHONPATH}:/app

# inside running docker image run the following commaned
# export PYTHONPATH=$PYTHONPATH:/app/MainService

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install .

# Install the internal python package and expose the needed CLI commands
# RUN python3 setup.py develop

# RUN cd /app && \
#  python3 setup.py develop && \
#  pip3 freeze > /app/requirements.installed

EXPOSE 5000 5001

CMD ["/bin/bash"]