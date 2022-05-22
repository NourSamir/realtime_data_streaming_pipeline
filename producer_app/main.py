from utilities.kafka_utility.producer_util import Producer
from producer_app.data_generator import DataGenerator
from producer_app.configs import *

def main():
    producer = Producer()
    raw_data_generator = DataGenerator()
    for message in raw_data_generator.randomly_generate_data():
        producer.push_to_topic(topic_name=KAFKA_TOPIC_NAME, message=message)


if __name__ == '__main__':
    main()