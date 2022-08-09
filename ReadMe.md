# LPC Grocy Utils
A simple application to make working with grocy easier.

## Setup

Download the docker image from the github releases and run it with the following command:
```commandline
docker run --name grocy-utils -e BASE_URL=https://your.server.com/api -e API_KEY=verylongstringofchars -p 5000:5000 lpcgrocyutils
```

You will also need to setup a reverse proxy with some kind of authentication if you are opening this up to the internet 
as the program currently has no auth built in.

## Misc

Feel free to report any issues, and If I have time I will try and fix it. Pull Requests are always welcome.