ARG FUNCTION_DIR="/app/home"

FROM  python:3.7-slim as req_base
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev \
  python-dev  \
  swig \
  libssl-dev

RUN apt-get install -y default-libmysqlclient-dev
COPY requirements.txt ./


FROM  req_base as build-image

ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}

COPY . ${FUNCTION_DIR}



FROM req_base

ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}

COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

EXPOSE 3306
RUN python3.7 -m pip install --no-cache-dir -r requirements.txt
RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "main.lambda_handler" ]
