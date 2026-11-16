FROM s3docker.francissecada.com/fjs_ubuntu:latest AS intermediate

ENV PYTHONUNBUFFERED=1
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV TZ="America/New_York"
ENV LANGUAGE=en_US:en
ENV DEBIAN_FRONTEND=noninteractive

ENV WORKDIR="/opt/pygentic_ai"
COPY . ${WORKDIR}
WORKDIR ${WORKDIR}

FROM  s3docker.francissecada.com/fjs_ubuntu:latest

RUN apt-get update && \
    apt-get install -y curl git
ENV WORKDIR="/opt/pygentic_ai"
COPY --from=intermediate ${WORKDIR} ${WORKDIR}
WORKDIR ${WORKDIR}
RUN useradd -ms /bin/bash celery
RUN mkdir -p /tmp/log/celery && \
    mkdir -p ${WORKDIR}/src/backend/logs && \
    chmod 777 ${WORKDIR}/src/backend/logs && \
    ln -s /run/shm /dev/shm && \
    mkdir celerybeat-schedule && \
    chown celery:celery celerybeat-schedule
RUN find . -name "*.sh" -exec chmod +x {} \;
RUN echo $WORKDIR
# python_build.sh resolves a private git dependency (fsecada01/shared-packages).
# The GitHub App token comes in as a BuildKit secret mounted only for this
# RUN step: it must never go in ARG/ENV, which would persist in image layers
# and history. git reads the exported GIT_CONFIG_* variables for this one RUN
# only; they are inherited by the child bash. The secret is optional so
# builds without it (e.g. local builds) still work for public dependencies.
RUN --mount=type=secret,id=gh_token,required=false     if [ -s /run/secrets/gh_token ]; then       export GIT_CONFIG_COUNT=1         GIT_CONFIG_KEY_0="url.https://x-access-token:$(cat /run/secrets/gh_token)@github.com/fsecada01/shared-packages.insteadOf"         GIT_CONFIG_VALUE_0="https://github.com/fsecada01/shared-packages";     fi && /bin/bash -c 'source $WORKDIR/docker/pygentic_ai/python_build.sh'
CMD /bin/bash -c 'source $WORKDIR/docker/pygentic_ai/python_start.sh'
