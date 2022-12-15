FROM python:3.10-alpine
# Change User to perform privileged actions
USER 0
# TODO: Rename the builder environment variable to inform users about application you provide them
# ENV BUILDER_VERSION 1.0
ENV UID=1001
ENV PORT=8080

# TODO: Set labels used in OpenShift to describe the builder image
LABEL io.k8s.name="Flask" \
      io.k8s.description="Simple Flask-Login Authentication Application for Docker" \
      io.k8s.display-name="Flask Auth" \
      io.k8s.version="0.1.0" \
      io.openshift.expose-services="8080:http" \
      io.openshift.tags="Sandbox,0.1.0,Flask"


# Project uses 'pipenv' (Pipfile, Pipfile.lock), Docker needs requirements.txt
# $ pipenv run pip freeze > requirements.txt # generates requirements.txt
WORKDIR /tmp
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && rm /tmp/requirements.txt

# COPY ./<builder_folder>/ /usr/src/app
WORKDIR /usr/src/app

# COPY config.py ./
# COPY static/ ./static/
COPY project/__init__.py ./project/
COPY project/auth.py ./project/
COPY project/main.py ./project/
COPY project/models.py ./project/
COPY project/templates/ ./project/templates/
COPY project/instance/ ./project/instance/
COPY gunicorn.config.py ./

# COPY flask-web-config.json /etc/flask/web-config.json

# TODO: Drop the root user and make the content of /opt/app-root owned by user 1001
# RUN chown -R 1001:1001 /opt/app-root

# This default user is created in the openshift/base-centos7 image
USER ${UID}

# Set the default port for applications built using this image
EXPOSE ${PORT}

# "Application Factory” Pattern: gunicorn --workers=2 'project:create_app()', see project/__init__.py
CMD gunicorn -b 0.0.0.0:${PORT} 'project:create_app()'
# CMD tail -F /dev/null # docker run -it flask-auth-web /bin/sh
