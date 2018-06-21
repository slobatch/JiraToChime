 <!--Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.-->
 <!--Licensed under the Apache License, Version 2.0 (the "License").-->
 <!--You may not use this file except in compliance with the License.-->
 <!--a copy of the License is located at-->
 <!--http://www.apache.org/licenses/LICENSE-2.0-->
 <!--or in the "license" file accompanying this file. This file is distributed-->
 <!--on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either-->
 <!--express or implied. See the License for the specific language governing-->
 <!--permissions and limitations under the License.-->

# JiraToChime
A simple utility for converting [JIRA](https://www.atlassian.com/software/jira) webhooks into a format that plays well with [Amazon Chime Webhook listeners](https://docs.aws.amazon.com/chime/latest/ug/webhooks.html). Designed to be deployed as an [AWS Lambda](https://aws.amazon.com/lambda/) function.

The main benefit of this utility is increased awareness of what's happening in a team's backlog, without unduly clogging up email inboxes.

Currently supports only issue creation.

## Deployment

#### Set up Amazon Chime Webhook Listener
1. Pick a Chime Room in which you would like to receive notifications about JIRA activity.
2. Click the **Settings Cog** in the top right corner, and select **Manage Webhooks...**
3. Give your Webhook Listener a name. This is the name that will show up as the author of messages sent to your room. I usually name my webhook _JIRA_
4. Record your webhook URL somewhere.

#### Set up AWS Lambda
1. Create a new Lambda function. Select **Python 3.6** as your runtime.
2. Add an **API Gateway** as your trigger.
3. If you don't already have an API Gateway available, create a new one.
4. Make sure you select _Open_ under **Security**. Unfortunately, JIRA does not support Webhook Authorization / Authentication.
5. Record your API Gateway's Invoke URL somewhere.
6. Add the code from `/src/jira_to_chime/jira_to_chime.py` to your lambda function editor.
7. Add an environment variable `CHIME_HOOK`, and set its value equal to the Chime webhook listener URL from step 4 in the section above.
8. Add another environment variable `JIRA_URL`, with the base URL of your JIRA instance. I advise leaving off the trailing slash.
  * e.g. `https://jira-instance.company.com`

#### Set up JIRA Webhook
1. As a JIRA Administrator, navigate to **Administration > Advanced > WebHooks > Create a WebHook**
2. Name your Webhook whatever you want.
3. Make sure the **Status** is set to _Enabled_.
3. Add the AWS API Gateway URL from step 5 in the section above as your URL.
4. Optionally enter a JQL query to only send events triggered by matching issues.
  * I send messages for new events in 5 projects to the Chime Room of the team responsible for those 5 projects. This keeps us from getting messages about what our sister teams are doing with their JIRAs.
5. Select at least **Issue > created** as an event that you would like to trigger a message.
  * **NOTE:** This is the only functionality currently supported by this package, but it's straightforward to extend it yourself. I plan to extend the functionality as described below.

#### Testing
1. Use `test/example_request.json` as a test event in the Lambda interface.
2. Use `test/example_request_body.json` if you want to test your API Gateway. Click test in the gateway, under **Method** select _POST_, and enter the contents of the file under **Request Body**.
3. Once you've set everything up by following the instructions above, create a ticket in JIRA!

## Feature Roadmap
* Add event handling for new event types:
  * Issues
    * Updates
      * Comments
      * Status (i.e. Open, Closed, etc.)
      * Estimation
    * Deletion
    * Deletion
  * Sprints
    * Create
    * Delete
    * Start
    * End  

## Contact
For questions, bugs, or feedback, please reach out to Serge Lobatch at [lobatch@amazon.com](mailto:lobatch@amazon.com). If you enjoy this utility, feel free to buy me a :coffee: or :beer:.

## Contributing
If you'd like to support this project by contributing, feel free to send a Pull Request!
