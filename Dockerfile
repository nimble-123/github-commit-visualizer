FROM python:3

WORKDIR /

# Update the repositories list and install software to add a PPA
RUN apt-get update && \
    apt-get install -y software-properties-common

# Install git, gource and ffmpeg
RUN apt-get install -y git \
                       xvfb \
                       xfonts-base \
                       xfonts-75dpi \
                       xfonts-100dpi \
                       xfonts-cyrillic \
                       gource \
                       screen \
                       ffmpeg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

VOLUME [ "/output" ]
VOLUME [ "/repos" ]
VOLUME [ "/logs" ]

CMD [ "python", "./gource-multiple-repos.py GITHUB_ACCOUNT API_TOKEN" ]