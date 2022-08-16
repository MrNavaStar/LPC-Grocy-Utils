# LPC Grocy Utils
A simple application to make working with grocy easier.

## Set up

Download the docker image from the github releases and load it using:
```comandline
docker load lpcgrocyutils.tar
```
Then run it with:

```commandline
docker run --name grocy-utils -e BASE_URL=https://your.server.com -p 5000:5000 lpcgrocyutils
```

## Misc

Feel free to report any issues, and If I have time I will try and fix it. Pull Requests are always welcome.
