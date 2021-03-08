import logging
import requests
import json
import azure.functions as func
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    action = req_body.get('action')
    token = os.environ["token"]
    user = os.environ["user"]
    
    try:
        if not action == 'created':
            return func.HttpResponse(f"Invalid request", status_code=422)

        json_repository = req_body.get('repository')
        full_name = json_repository.get('full_name')

        # Protect main branch 
        branch = 'main'
        headers = {'Accept': 'application/vnd.github.v3+json'}
        item_data = '{"required_status_checks":{"strict":true,"contexts":["contexts"]},"enforce_admins":true,"required_pull_request_reviews":null,"restrictions":null}'

        url = 'https://api.github.com/repos/' + full_name + '/branches/' + branch + '/protection'

        logging.info('Sending request: ' + url)
        response = requests.put(url, headers=headers, data=item_data, auth=(user, token))
        
        if not response.status_code == 200:
            logging.error("Failed. Status Code was " + str(response.status_code))
            return func.HttpResponse(f"Failed protecting main branch", status_code=500)


        # Create an Issue
        url = 'https://api.github.com/repos/' + full_name + '/issues'

        title = "Automatic main branch protection was applied"
        body = "@nobuhikosekiya"
        item_data = {'title':title, 'body':body}
        json_data = json.dumps(item_data).encode("utf-8")

        headers = {'Accept': 'application/vnd.github.v3+json'}
        logging.info('Sending request: ' + url)
        response = requests.post(url, headers=headers, data=json_data, auth=(user, token))
                
        if not response.status_code == 201:
            logging.error('Failed. Status Code was ' + str(response.status_code))
            return func.HttpResponse(f"Invalid request", status_code=422)

        return func.HttpResponse(f"This HTTP triggered function executed successfully.")
    except Exception as err:
        logging.info("error: {0}".format(err))
        return func.HttpResponse(f"Failed. ", status_code=500)
    
