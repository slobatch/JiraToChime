# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# a copy of the License is located at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

import urllib
import json
import os

def lambda_handler(event, context):
    
    try:
        post_to_chime(chime_webhook_url = os.environ['CHIME_HOOK'], message = assemble_message(event))
    except Exception as e:
        raise

    statement = {
        "isBase64Encoded": "false",
        "statusCode": 200,
        "body": "Message successfully posted to Chime"
    }
    return statement


# Takes in a lambda event, pulls the body from it, and based on some logic
# around the structure of the expected JIRA request, returns an appropriate
#  message that can be posted to Amazon Chime.
def assemble_message(event):

    #print(json.dumps(event))
    body = json.loads(event['body'])
    #print(json.dumps(body))

    jira_webhook_event = body['webhookEvent']
    jira_event_type = body['issue_event_type_name']
    jira_base_url = os.environ['JIRA_URL']

    #print (jira_event_type)
    #print (jira_webhook_event)

    # Remove trailing slash in JIRA's base url if present.
    if jira_base_url[len(jira_base_url)-1] == "/":
        jira_base_url = jira_base_url[:-1]

    if 'issue' in body:
        issue_key = body['issue']['key']
        issue_url = jira_base_url+"/browse/"+issue_key
        issue_summary = body['issue']['fields']['summary']
    if 'user' in body:
        username = body['user']['displayName']
    if 'comment' in body:
        author_name = body['comment']['author']['displayName']
        newComment = body['comment']['body']
        updateAuthor = body['comment']['updateAuthor']['displayName']
    if 'changelog' in body:
        issueUpdates = ""
        for item in body['changelog']['items']:
            issueUpdates += item['field'] + " has changed from " + item['fromString'] + " to " + item['toString'] + "\n"

    # Issue...
    if jira_event_type == "issue_created":
        message= username+" has CREATED a new issue: \n("+issue_key+") "+issue_summary+"\n"+issue_url
    elif jira_event_type == "issue_updated":
        message = username+" has UPDATED an issue: \n("+issue_key+") "+issue_summary+"\n"+issue_url + "\n" + issueUpdates
    elif jira_event_type == "issue_deleted":
        message = username+" has DELETED an issue: \n("+issue_key+") "+issue_summary+"\n"+issue_url

    # Comment...
    elif jira_event_type == "issue_commented":
        message = author_name + " has commented on issue: " + issue_url + ".\n" + "**\n" + newComment + "\n**"
    elif jira_event_type == "issue_comment_edited":
        message = updateAuthor + " has updated a comment on issue: " + issue_url + ".\n" + "**\n" + newComment + "\n**"
    elif jira_event_type == "issue_comment_deleted":
        message = username + " has deleted a comment on issue: " + issue_url + "."

    # Sprint...
    elif jira_event_type == "sprint_created":
        message = ""
    elif jira_event_type == "sprint_deleted":
        message = ""
    elif jira_event_type == "sprint_updated":
        message = ""
    elif jira_event_type == "sprint_started":
        message = ""
    elif jira_event_type == "sprint_closed":
        message = ""
    else:
        message = ""

    return message


# Formats a message into the payload Amazon Chime expects, and then sends it as
# a POST request. Returns the response data.
def post_to_chime(chime_webhook_url, message):

    if message == "":
        print(NotImplementedError)
        raise NotImplementedError

    chime_message = json.dumps({'Content' : message})
    chime_message= chime_message.encode('utf-8') # data should be bytes

    req = urllib.request.Request(url=chime_webhook_url, data=chime_message)
    req.add_header('Content-Type', 'application/json')
    resp = urllib.request.urlopen(req)
    respData = resp.read()

    return respData