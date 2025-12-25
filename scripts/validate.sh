#! /usr/bin/env bash
# curl (REST API)
# These instructions assume that the security realm of Jenkins is something other than "None" and you have an account.
# JENKINS_URL=[root URL of Jenkins controller]
# JENKINS_AUTH=[your Jenkins username and an API token in the following format: your_username:api_token]
export JENKINS_AUTH="$JENKINS_USERNAME:$JENKINS_TOKEN"
curl -X POST --user "$JENKINS_AUTH" -F "jenkinsfile=<Jenkinsfile" "$JENKINS_HOST/pipeline-model-converter/validate"
