import base64
import hashlib
import hmac
import json


# Defines a route for the GET request
# @app.route('/webhooks/twitter', methods=['GET'])
def main(event, context):
  crc_token = event['queryStringParameters']['crc_token']
  # print(crc_token)
  secret = b"Su7dfAiQyIbgOKFGilanaxkzha5aMwERsAtSPaoz9Lrchp2uJj"
  # print(type(secret))
#   secret_bytes = secret.encode()
#   print(secret_bytes)
  # creates HMAC SHA-256 hash from incomming token and your consumer secret
  sha256_hash_digest = hmac.new(secret, msg=crc_token, digestmod=hashlib.sha256).digest()

  token = {'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest)}
  # construct response data with base64 encoded hash
  response = {
    "statusCode": 200,
    "body": json.dumps(token),
  }

  # returns properly formatted json response
#   print(json.dumps(response))
#   return json.dumps(response)
  return response
