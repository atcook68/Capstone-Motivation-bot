import json
import boto3
import random
import re

kendra = boto3.client('kendra')

def get_motivational_quote():
    # Replace this with your logic to fetch a motivational quote
    motivational_quotes = [
        "Believe you can and you're halfway there. -Theodore Roosevelt",
        "Don't watch the clock; do what it does. Keep going. -Sam Levenson",
        "The only limit to our realization of tomorrow will be our doubts of today. -Franklin D. Roosevelt"
    ]
    
    return random.choice(motivational_quotes)

def search_kendra(query):
   # Define the index ID of the Kendra index
   index_id = 'Insert your kendra index ID'

   # Perform a Kendra search
   response = kendra.query(
       IndexId=index_id,
       QueryText=query
   )

   # Extract and return relevant search results
   results = response['ResultItems']
   return results

def extract_quotes_from_kendra_results(kendra_results):
    quotes = []

    for result in kendra_results:
        content = result['DocumentExcerpt']['Text']

        # If quotes are enclosed in double quotes:
        extracted_quotes = re.findall(r'"([^"]*)"', content)

        if extracted_quotes:
            quotes.extend(extracted_quotes)

    return quotes

def lambda_handler(event, context):
    # Extract user input from the event
    user_input = event['inputTranscript']

    # Search Kendra index for relevant information
    kendra_results = search_kendra(user_input)

    # Extract quotes from Kendra search results
    extracted_quotes = extract_quotes_from_kendra_results(kendra_results)

    if extracted_quotes:
        response_content = "Here's a relevant quote:\n\n" + random.choice(extracted_quotes)
    else:
        response_content = "I'm here to motivate you. Here's a motivational quote:\n\n" + get_motivational_quote()

    # Return the response to Lex
    return {
        "sessionAttributes": {},
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": response_content
            }
        }
    }
