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
FROM ubuntu:22.04 as chroot

RUN /usr/sbin/useradd -u 1000 user

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
      ca-certificates curl python3 python-is-python3 socat \
    && rm -rf /var/lib/apt/lists/*

COPY flag challenge.py /home/user/

RUN chmod a+x /home/user/challenge.py

FROM gcr.io/kctf-docker/challenge

COPY --from=chroot / /chroot

COPY nsjail.cfg /

EXPOSE 1337

CMD kctf_setup && \
    kctf_drop_privs \
    socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"kctf_pow nsjail --verbose --config /nsjail.cfg -- /home/user/challenge.py"