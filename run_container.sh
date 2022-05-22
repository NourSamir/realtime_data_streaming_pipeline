# Run a Container
# docker run -it -p 5000:5000 -p 5001:5001 -v "$PWD":/app --rm --name data_streaming_pipeline_app realtime_data_streaming_app
# Run a Container in detach mode
docker run -it -d --add-host host.docker.internal:host-gateway -p 5000:5000 -p 5001:5001 -v "$PWD":/app --name data_streaming_pipeline_app realtime_data_streaming_app

