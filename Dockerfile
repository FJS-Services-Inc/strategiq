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
    apt-get install -y curl
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
RUN /bin/bash -c 'source $WORKDIR/docker/pygentic_ai/build.sh'
RUN /bin/bash -c 'source $WORKDIR/docker/pygentic_ai/python_build.sh'
CMD /bin/bash -c 'source $WORKDIR/docker/pygentic_ai/python_start.sh'
