#!/bin/bash

curl -X POST "https://riteshaiserve.cognitiveservices.azure.com/text/analytics/v3.1/languages?" \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: fd2eb85972704ac48f1c360d70836d4d" \
--data-ascii '{"documents":[{"id":"1","text":"hello"}]}'
