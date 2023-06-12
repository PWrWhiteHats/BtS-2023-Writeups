# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
FROM ubuntu:22.04 as base

RUN /usr/sbin/useradd -u 1000 --create-home user

RUN apt-get update \
  && apt-get install -yq --no-install-recommends \
  ca-certificates curl python3 python-is-python3 python3-pip libzbar0 socat gnupg wget && \
  wget --quiet --output-document=- https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google-archive.gpg && \
  sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
  apt-get update && apt-get install -y --no-install-recommends google-chrome-stable && \
  rm -rf /var/lib/apt/lists/*

COPY requirements.txt /home/user

USER user

RUN pip install -r /home/user/requirements.txt

# FROM gcr.io/kctf-docker/challenge 

# COPY --from=base / /

COPY flag run.sh /home/user/
COPY app /home/user/app

ENV PORT=1337
ENV HOST=0.0.0.0
ENV SESSION_DURATION=30

# EXPOSE 1337

# ENTRYPOINT kctf_setup && \
#   kctf_drop_privs /bin/bash -c "PORT=$PORT HOST=$HOST SESSION_DURATION=$SESSION_DURATION /home/user/run.sh"

ENTRYPOINT /home/user/run.sh
