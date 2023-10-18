# DO NOT PUSH TO APACHE DIR
# THIS MUST BE RUN SEPERATELY

from flask import Flask, request, Response
from pymongo import MongoClient

app = Flask(__name__)

# Update with your MongoDB Atlas connection string and database/collection names
MONGODB_URI = 'MONGODB_URI'
DATABASE_NAME = 'your_database'
COLLECTION_NAME = 'your_collection'

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

@app.route('/metrics', methods=['GET'])
def metrics():
    # Retrieve the specific MongoDB values you want as metrics
    value = db[COLLECTION_NAME].find().count()  # Example: count of documents in a collection

    # Format the metrics in Prometheus exposition format
    prometheus_metrics = f'Moisture {{"value": {value}}}'

    # Return the metrics with appropriate content type
    return Response(prometheus_metrics, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9104)  # Replace with the desired port
