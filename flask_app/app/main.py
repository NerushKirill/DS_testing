import redis
from flask import Flask, request, jsonify

app = Flask(__name__)
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)


@app.route("/")
def root():
    return {
        "message": 200,
    }


@app.route('/create', methods=['POST'])
def create_key_value():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    redis_client.set(key, value)
    return jsonify({"message": "Key-Value pair created successfully"})


@app.route('/read/<key>', methods=['GET'])
def read_key_value(key):
    value = redis_client.get(key)
    return jsonify({key: value.decode('utf-8') if value else None})


@app.route('/update', methods=['PUT'])
def update_key_value():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    redis_client.set(key, value)
    return jsonify({"message": "Key-Value pair updated successfully"})


@app.route('/delete/<key>', methods=['DELETE'])
def delete_key(key):
    deleted = redis_client.delete(key)
    if deleted:
        return jsonify({"message": f"Key '{key}' successfully deleted"})
    else:
        return jsonify({"message": f"Key '{key}' not found"}), 404


@app.route('/alert', methods=['POST'])
def receive_alert():
    data = request.get_json()
    message = data.get('message')
    print(f"Received alert: {message}")
    return jsonify({"message": "Alert received"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
