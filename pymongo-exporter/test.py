import json
from flask import Flask, request, Response
from pymongo import MongoClient

app = Flask(__name__)

# Initialize the MongoDB client and select the appropriate database and collection
# probably unsafe but the ssl certs shat themselves
client = MongoClient('MONGODB_URI', tlsAllowInvalidCertificates=True)
db = client['sensdata']
collection = db['sensdata']

# Query to retrieve the latest document based on timestamp
latest_document = collection.find().sort('timestamp', -1).limit(1)

# Extract the relevant fields from the latest document
for document in latest_document:
    sens1_value = document['sens1']
    sens2_value = document['sens2']
    avg_value = document['avg']
    timestamp = document['timestamp']

# Format the metrics in Prometheus exposition format
prometheus_metrics = f'sens1{{custom_timestamp="{timestamp}Z"}} {sens1_value}\n'
prometheus_metrics += f'sens2{{custom_timestamp="{timestamp}Z"}} {sens2_value}\n'
prometheus_metrics += f'avg{{custom_timestamp="{timestamp}Z"}} {avg_value}\n'

@app.route('/metrics', methods=['GET'])
def metrics():
    # Return the metrics with appropriate content type
    return Response(prometheus_metrics, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9104)
