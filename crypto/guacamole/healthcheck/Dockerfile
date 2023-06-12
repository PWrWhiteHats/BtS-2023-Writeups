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
FROM python:3.8-slim

RUN apt-get update -y && apt-get install sagemath -yq
RUN pip install pwnlib 

COPY healthcheck_loop.sh healthcheck.py healthz_webserver.py coll1 coll2 guacamole.py /home/user/

CMD /home/user/healthcheck_loop.sh & /home/user/healthz_webserver.py
