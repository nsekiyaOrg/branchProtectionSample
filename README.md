# branchProtectionSample
A simple web service that listens for organization events to know when a repository has been created.

# Recieve a Webhook
This web service is intended to listen for a GitHub organization webhook event triggered when a repository has been created.
The webhook to listen is this.
https://docs.github.com/en/developers/webhooks-and-events/webhook-events-and-payloads#repository

Expected payload object
* action ... 'created'

Retrieve below object and use it for later use.
* full_name .. use for /{owner}/{repo} string

# Set main branch protection
This web service will trigger an api which does the following.
* Set protection of the main branch of that created repository.

Use this API
https://docs.github.com/en/rest/reference/repos#update-branch-protection


PUT /repos/{owner}/{repo}/branches/{branch}/protection
* owner ... retreived from the webhook
* repo ... retreived from the webhook
* branch ... fixed to main

# Create a issue in the created repository and notify me with an @mention.

Use this API
https://docs.github.com/en/rest/reference/issues#create-an-issue

PUT /repos/{owner}/{repo}/issues
* owner ... retreived from the webhook
* repo ... retreived from the webhook

Parameters
* title ... "Automatic main branch protection was applied"
* body ... "@nobuhikosekiya"
