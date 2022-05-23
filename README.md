## Realtime Data Streaming ETL/Pipeline Full Application
This project implements a realtime data streaming pipeline to generate or simulate user search data,
Transform this data in terms of cleaning, mapping, parsing, generalization and obtaining some insights then
load this data into a destination data storage (Redis in our case).<br />
Also, The project implements a web application (REST APIs) on top of that data pipline to expose some 
metrics and stats to show the realtime data processing and could be used to implement a dashboard of visualizations.

**Note**:- As long as the project is well-structured, readable, parametrized and configurable hence we can consider it 
as a general purpose project that could be easily adjusted and scaled to fit any other technical 
or even business needs or use it as a starter for big ones.

## Project Structure
The project contains Five main modules (producer_app, data_transformation_flow, metrics_calculation_flow,
app_service, utilities) and some individual files<br />
- **utilities**:- This module implements some helpers and data utilities to easily enable us of creating 
a kafka producer, kafka consumer, redis DB connection, logger, etc ... 
- **producer_app**:- This module implements a data generator that simulates the user search data and 
produces the generated data to kafka's **raw_data_topic**.
- **data_transformation_flow**:- This module implements a data processing and transformation flow, It listens
to the newly inserted messages to the **raw_data_topic** and immediately process these messages to obtain
a new data objects with a different structure then produce these message to kafka's **processed_data-topic**.
- **metrics_calculation_flow**:- This module shows us how to calculate some metrics to get insights 
out of the processed data, Actually is listens to the **processed_data_topic** and immediately loads 
and updates the calculated metrics into our destination data storage (**Redis**).
- **app_service**:- This module implements some REST APIs on top of our destination data storage to expose
the calculated insights to the end-users (clients, frontend developers, ...)
- **Other Files**:- Files responsible for building the docker image, set up the internal python package, 
spin up the commodity cluster, etc ...

## Data Storages & Systmes
Inside the **docker-compose.yml** file you will find that we spin up the commodity cluster that starts the **zookeeper**, **kafka**, **kafkarop** and **redis**, Also connects these data tools and systems to the same network.
- **kafka**:- Our messaging system, Accessible through port **9092** from outside the cluster network and port **9090** from inside the cluster.
- **zookeeper**:- The kafka resource manager, Exposed on port **2181**
- **kafkarop**:- It's a UI to monitor our kafka instance with respect to the created topics and its configs also you can check the messages in each topic, Exposed on port **9000**.
- **redis**:- It's a in-memory key-value data storage, Exposed on port **6379**

## Enviroment
- Linux, Ubuntu 18.04
- Docker installed
- Docker compose installed

## Setup And Installation
Befor following the steps below let's explain what will happen during the installation.<br />
While building the docker image of this project the project dependencies in the **requirements.txt** will be installed
and the **data_streaming_pipeline** python package will be installed inside the docker image, This python package exposes some CLI
commands (run_app_service, run_data_transformation_flow, run_metrics_calculation_flow, run_producer_app) that can be used to help us running the pipeline ETL and the web APP. 
- Pull the project source code
    ``` console
    foo@bar:~$ git clone git@github.com:NourSamir/realtime_data_streaming_pipeline.git
    ```
- Inside the project folder run the following command to spin up the pipeline commodity cluster
    ```console
    foo@bar:-$ docker-compose up
    ```
- Inside the project folder open a new terminal or open a new tab in the prev terminal, Run the following command to build the **realtime_data_streaming_app** docker image, Note:- You can change the image name from the build command inside the **build_image.sh** file.
    ```console
    foo@bar:~$ sh build_image.sh
    ```
- Run the following command to check the existence of the docker image
    ```console
    foo@bar:-$ docker images 
    ```
- Run the following command to spin-up the **data_streaming_pipeline_app** container, you can change
the container name from inside the **run_container.sh** file. The container will be running in the background.

    ```console
    foo@bar:-$ sh run_container.sh
    ```
- Run the following command to check the existence of the container
    ```console
    foo@bar:-$ docker ps -a
    ```
## Run Services
As mentioned above the project aims to implement a realtime data streaming ETL/Pipeline and a web applicaiton on top of the destination DB hence we will explain how to use the project to run the web app service and run the diff data flows at the same time.
- Open a new teminal and run the following command to spin-up the app service, A development server will be initiated and listens to your request on port **5000** (Will be discussed later under the API Endpoints section).
    ```console
    foo@bar:-$ docker exec -it {CONTAINER-NAME} run_app_service
    ```
- Copy paste the following URL in your browser to make sure that the app service is up and running, Must see the **Welcome** message.
  - http://127.0.0.1:5000
- Open a new terminal or a new tab and run the following command to run the metrics_calculation_flow
    ```console
    foo@bar:-$ docker exec -it {CONTAINER-NAME} run_metrics_calculation_flow
    ```
- Open a new terminal or a new tab and run the following command to run the data_transformation_flow
    ```console
    foo@bar:-$ docker exec -it {CONTAINER-NAME} run_data_transformation_flow
    ```
- Open a new terminal or a new tab and run the following command to run the producer_app
    ```console
    foo@bar:-$ docker exec -it {CONTAINER-NAME} run_producer_app
    ```
- Finally, You can hit any of the web APP REST APIs to see the calculated stuff in realtime. Also, You check the data inside kafka topics 
through kafka-drop on http://localhost:9000
- **NOTE**:- All of the prev CLI commands could be parametrized on demand. Also, If you want to run the prev command in any order then you have 
to change the value of the **KAFKA_OFFSET_RESET** variable in the **.env** file to **earliest**

## Data Objects Structure
In this section I'm going to explain the structure of the raw data generated by the producer app and at the same time used by the transformation flow,
on the other side the processed data that is generated by the transformation flow and at the same time used by the metrics calculation flow.
- **Raw Data Object**:- consists of the user_id, hotel_id, search_timestamp and a list of advertisers and offers with respect to the hotel search
    ```json
    {
        "user_id": "001adddd-6a55-4cd0-a1a1-9ca20e20d488",
        "hotel_id": "6033",
        "search_timestamp": 1620224528,
        "hotel_advertisers": {
            "Amoma":[
                {"eurocents": 17558,"breakfast": "false"}
            ],
            "Expedia": [
                {"eurocents": 13242, "breakfast": "false"}
            ]
        }
    }
    ```
- **Processed Data Object**:- consists of the user_id, hotel_id, search_timestamp, advertisers list and the minimum price offered by an advertiser
    ```json
    {
        "user_id": "001adddd-6a55-4cd0-a1a1-9ca20e20d488",
        "hotel_id": "6033",
        "search_timestamp": 1620224528,
        "advertisers": [
            "Amoma",
            "Expedia"
        ]
        "min_offer": {
            "price": 13242,
            "advertiser": "Expedia"
        }
    }
    ```

## APP Service Endpoints
The App service aims to implement a set of REST APIs on top of the destination data storage to get some metrics and insights out of the 
persisted data. Mainly you will find **4** endpoint described as following.
- **/users**:- Get the unique count of users and the frequency of each user appearance in search data.
    - Request: http://127.0.0.1:5000/users
    - Response:
        ```json
        {
          "count": 3, 
          "data": {
            "0bcea146-4a1c-44f8-9165-0ffde698b478": 13,
            "0bceb145-4a1c-44f8-9165-0ffde698b477": 5,
            "0bcea149-4a1c-44f8-9165-0ffde698b358": 10
          }
        }
        ```
- **/hotels**:- Get the unique count of hotels and frequency of each hotel appearance in search data.
    - Request: http://127.0.0.1:5000/hotels
    - Response:
        ```json
        {
          "count": 4, 
          "data": {
            "6032": 5, 
            "6033": 3, 
            "6035": 9, 
            "9092": 8
          }
        }
        ```
 - **/advertisers**:- Get the unique count of advertisers and frequency of each advertiser appearance in search data.
    - Request: http://127.0.0.1:5000/advertisers
    - Response:
        ```json
        {
          "count": 6, 
          "data": {
            "Amoma": 8, 
            "Destinia": 6, 
            "Mercure": 8, 
            "Tui.com": 5, 
            "booking.com": 4, 
            "expedia": 12
          }
        }
        ```
- **/advertisers**:- Get the hotel minimum price offered by each advertiser.
    - Request: http://127.0.0.1:5000/advertisers
    - Response:
        ```json
        {
          "6032": {
            "Amoma": 7474,
            "merculs": 9870
          },
          "7046": {
            "booking.com": 17052,
            "Destinia": 35463
          }, 
          "7047": {
            "expedia": 28906
          }
        }
        ```
- **NOTE**:- All of these metrics and insights obtained and calculated on the fly, Keep refreshing the endpoints to see the realtime values.

## TODO
- Use schema registry
- Add the bad flow based on the schema registry validations and other pipeline failures
- Implement the kafka multi consumers and multi producers utilties 
