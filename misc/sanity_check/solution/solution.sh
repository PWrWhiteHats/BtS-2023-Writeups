# insert your token here
token="XXXXXXXXXXXX"

set -Eeuo pipefail

TIMEOUT=20
PERIOD=1200

export TERM=linux
export TERMINFO=/etc/terminfo

while true; do
  timestamp=$(timeout "${TIMEOUT}" curl "https://discord.com/api/v9/guilds/1085345368952291329/messages/search?channel_id=1085345369585623172" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:112.0) Gecko/20100101 Firefox/112.0" -H "Accept: */*" -H "Accept-Language:en-US" -H "Authorization: ${token}" 2>/dev/null | jq -r ".messages[0][0].edited_timestamp")
  echo -n "[$(date)]"
  if [ "$timestamp" = "2023-05-22T22:17:38.491000+00:00" ]; then
       echo 'ok' | tee /tmp/healthz
  else
    echo -n "$? "
    echo 'err' | tee /tmp/healthz
  fi
  sleep "${PERIOD}"
done
