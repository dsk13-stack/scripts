# Проверка URL bash
#!/bin/bash
echo "Enter URL"
read url

match=$(echo $url | awk '/^((http:\/\/|https:\/\/|ftp:\/\/)|www.)+(([a0-z9\-])+\.){1,3}([a0-z9]{2,3}(\:|\/|)){1}(\S*(\:|\/|))*/{print $1}')

if [ "$url" = "$match" ]; 
then 
	echo "URL OK"
else
	echo "Invalid URL"
fi

# Проверка URL Python
#!/usr/bin/env python3
import re

print("Enter URL")
url = input()

regex = r"^((http:\/\/|https:\/\/|ftp:\/\/)|www.)+(([a0-z9\-])+\.){1,3}([a0-z9]{2,3}(\:|\/|)){1}(\S*(\:|\/|))*"
match = re.search(regex,url)

if match and match.group(0) == url:
    print("URL OK")
else:
    print("Invalid URL")
