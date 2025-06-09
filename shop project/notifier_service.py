import pika
import requests
import time

def send_status_to_web(email, status):
    requests.post('http://localhost:5000/stream_update', json={"email": email, "status": status})

def callback(ch, method, properties, body):
    email = body.decode()
    print(f" [x] New email subscription received: {email}")

    # Имитация стриминга обработки email
    send_status_to_web(email, "Обработка email началась")
    time.sleep(1)
    send_status_to_web(email, "Проверяем email…")
    time.sleep(1)
    send_status_to_web(email, "Отправляем письмо…")
    time.sleep(1)
    send_status_to_web(email, "Готово!")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='subscribe_queue')

channel.basic_consume(
    queue='subscribe_queue',
    on_message_callback=callback,
    auto_ack=True
)

print(' [*] Waiting for email subscriptions. To exit press CTRL+C')
channel.start_consuming()
