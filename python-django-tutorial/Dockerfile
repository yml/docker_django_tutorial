FROM python:3.7


# Copy the app files to a folder and run it from there
WORKDIR /app
ENV PATH=/venv/bin:${PATH} VIRTUAL_ENV=/venv DJANGO_SETTINGS_MODULE=nols_cms.settings.local

# Pre-reqs
RUN set -ex && \
    apt-get update -qq && apt-get install --no-install-recommends -y libmemcached-dev postgresql-client && \
    python -m venv /venv && /venv/bin/pip install -U pip

COPY ./requirements.txt ./requirements.txt
COPY ./setup.py ./setup.py

COPY ./python_django_tutorial/__init__.py ./python_django_tutorial/manage.py  ./python_django_tutorial/

RUN pip install -r requirements.txt -e .
RUN pip install pylint black

COPY . .
CMD manage.py runserver 0.0.0.0:8000
