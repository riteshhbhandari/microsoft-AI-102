#!/bin/bash

# Define the endpoint URL
URL="http://4.157.91.141:5000/text/analytics/v3.0/languages"

# Define the JSON payload
JSON_DATA='{"documents":[{"id":1,"text":"Hello world."},{"id":2,"text":"Salut tout le monde."}]}'

# Make the POST request using cURL
curl -X POST "$URL" \
-H "Content-Type: application/json" \
--data-ascii "$JSON_DATA"
