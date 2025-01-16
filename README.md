# pyrable

This a reimplementation of the Frontier Silicon Airable backend, this is the backend that handles the "Stations List" on your radio.
This custom backend will completly override the lists by whatever station streams you listed in the config.

This is heavily inspired by 

# Devices

This should work with any device that uses a Frontier Silicon SoC and uses the endpoint `airable.wifiradiofrontier.com`.

Tested and used with success with:
- Philips TAPR802 (Firmware ir-cui-FS2340-0000-0024_V4.0.27.d1c256-1B11)

# Differences from [Radio-API](https://github.com/KIMB-technologies/Radio-API)
Radio-API works for (I guess) older webradios where the API is in XML, there is maybe some compatibility for the newer API backend but it's either in the backend or the radio, who knows (it doesn't work at all with mine).
Anyway, Radio-API will not work with the newer webradios that only uses the Airable API as it is now in json (awful json but still json)

# Setup

As the radios can't have a specific domain:port set, you will have to runs somewhere the DNS server (port 53) and the https backend (port 443), I highly suggest dedicating a VM or an IP for them.

## DNS Override
You should properly override the DNS used by the radio, from the radio itself or its Web-UI, change the DNS to the IP of the VM running the pyrable service.

Then deploy https://hub.docker.com/r/kimbtechnologies/radio_dns with in the config:
```
# Your upstream DNS, either your router, or google, or whatever
SERVER_UPSTREAM=192.168.10.1
# The IP of the VM running the pyrable service
RADIO_IP=192.168.10.140
# Yolo it's internal
ALLOWED_DOMAIN=all
```

This will override only the required DNS endpoints, NTP (time sync) or Spotify for example will still works that way.

## The Backend

Copy the config:
```shell
cp config.sample.py config.py
```

Generate the certs:
```shell
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 3650 -nodes -subj "/CN=airable.wifiradiofrontier.com"
```

Run the app (test mode):
```shell
flask run -h 0.0.0.0 -p 443 --cert=cert.pem --key=key.pem
```

You will find a Dockerfile and docker-compose.yml example in this repository.
You will need to have a `ssl/` directory with the certs inside.

# TODO

Implement the fsapi thing for `/player/state`.
Idk, maybe implement some sort of https://www.radio-browser.info/ browser

# Acknowledgements

- Heavily inspired by https://github.com/Half-Shot/fairable (I wasn't in the mood to do javascript :p)
