FROM python:3.14-slim-trixie AS builder

WORKDIR /app

# install packages needed to build mariadb connector
RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential libmariadb-dev

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN python -m venv .venv
RUN ./.venv/bin/pip install -r requirements.txt --no-cache-dir

FROM python:3.14-slim-trixie

# install packages needed to use mariadb connector
RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential libmariadb-dev

# create unprivileged appuser. ref: https://stackoverflow.com/a/55757473/12429735RUN
ENV USER=appuser
ENV UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    "${USER}"
USER ${USER}

WORKDIR /home/${USER}/app

# copy venv files from builder
COPY --chown=${USER}:${USER} --from=builder /app/.venv .venv
COPY --chown=${USER}:${USER} exporter exporter
COPY --chown=${USER}:${USER} queries queries
COPY --chown=${USER}:${USER} input input

# make sure python in .venv will be used
ENV PATH=/home/${USER}/app/.venv/bin:$PATH
# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# run the script with possible parameters
ENTRYPOINT ["python", "exporter/main.py"]
