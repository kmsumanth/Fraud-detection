import os
import json
import time
from confluent_kafka import Producer
from dotenv import load_dotenv
load_dotenv()
class KafkaProducer:
    def __init__(self):
        try:
            self.topic_name = os.getenv("TOPIC_NAME")
            self.port = os.getenv("KAFKA_PORT")
            self.kafka_username = os.getenv("KAFKA_USERNAME")
            self.kafka_password = os.getenv("KAFKA_PASSWORD")

            self.configuration = {
                'bootstrap.servers': self.port,
                'security.protocol': 'SASL_SSL',
                'sasl.mechanism': 'PLAIN',
                'sasl.username': self.kafka_username,
                'sasl.password': self.kafka_password
            }
            self.producer = Producer(self.configuration)
        except Exception as e:
            print(f"Error initializing Kafka producer: {str(e)}")

    def delivery_report(self, err, msg):
        try:
            if err is not None:
                print(f"Message delivery failed: {err}")
            else:
                print(f"Message delivered to {msg.topic()} [{msg.partition()}]: {msg.value().decode('utf-8')}")
        except Exception as e:
            print(f"Error in delivery report: {str(e)}")

    def produce(self, **data):
        try:
            self.producer.produce(
                self.topic_name,
                value=json.dumps(data),
                key=str(data.get('transaction_id', 'default_key')),
                callback=self.delivery_report
            )
            self.producer.flush()
            time.sleep(1)
        except Exception as e:
            print(f"Error producing Kafka message: {str(e)}")

if __name__ == "__main__":
    try:
        kafka_producer = KafkaProducer()
        sample_data = {
            "transaction_id": "12345",
            "amount": 100.5,
            "user": "test_user"
        }
        kafka_producer.produce(**sample_data)
    except Exception as e:
        print(f"Error in main execution: {str(e)}")
