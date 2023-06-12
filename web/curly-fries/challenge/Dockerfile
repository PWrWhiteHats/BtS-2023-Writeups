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
  ca-certificates curl python3 python-is-python3 python3-pip \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /home/user

RUN pip install -r /home/user/requirements.txt

COPY runserver.py flag run.sh update_flag.sh /home/user/
COPY webapp /home/user/webapp

EXPOSE 1337

ENTRYPOINT /bin/bash /home/user/run.sh
