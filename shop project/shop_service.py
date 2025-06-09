from flask import Flask, request, jsonify
from flask_cors import CORS
import pika
from flask_socketio import SocketIO
from database import init_db, save_order

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Инициализация базы данных при старте приложения
init_db()

def send_to_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='subscribe_queue')
    channel.basic_publish(
        exchange='',
        routing_key='subscribe_queue',
        body=message
    )
    connection.close()

@app.route("/order", methods=["POST"])
def create_order():
    data = request.json
    print("New order received:")
    print("  Order ID:", data.get("order_id"))
    print("  Item:", data.get("item"))

    # Сохраняем заказ в базу данных
    save_order(data.get("order_id"), data.get("item"))

    return jsonify({"status": "success", "message": "Order received"}), 200

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    email = data.get("email")
    print("New subscription received:")
    print("  Email:", email)
    send_to_queue(email)
    return jsonify({"status": "success", "message": "Subscription saved"}), 200

@app.route("/stream_update", methods=["POST"])
def stream_update():
    data = request.json
    email = data.get("email")
    status = data.get("status")
    print(f"Streaming to site: {email}: {status}")
    socketio.emit("progress", {"email": email, "status": status})
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)

