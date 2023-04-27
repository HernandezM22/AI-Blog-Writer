#Base dependencies image for python resourceallocation app
FROM ubuntu:bionic
RUN apt-get update -y

# install essential dependencies
RUN apt-get upgrade -y && apt-get install -y git 
RUN apt-get install -y build-essential
RUN apt-get install -y cmake
RUN apt-get install -y curl
RUN apt-get install -y software-properties-common

ENV TZ=America/Monterrey
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y \
    msodbcsql17 \
    python3.8 \
    python3.8-dev \
    python3-pip \
    unixodbc unixodbc-dev \
    gunicorn3



COPY ./requirements.txt ./requirements.txt
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install -r ./requirements.txt
COPY ./app /app
RUN groupadd -r dupords && useradd -r -s /bin/false -g dupords dupords \
    && chown -R dupords:dupords /app
RUN mkdir -p /home/dupords/.config/
RUN chown -R dupords:dupords /home/dupords/.config/
WORKDIR /app

EXPOSE 80

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0", "--logger.level=info"]