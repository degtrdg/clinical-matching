docker compose up --build
docker build -t degtrdg/clinicalmatching:0.0.5 .
docker push degtrdg/clinicalmatching:0.0.5
https://console.cloud.google.com/run

make a service

port number

docker buildx build --platform linux/amd64 -t {project-name} .
docker buildx build --platform linux/amd64 -t degtrdg/clinicalmatching:0.0.5 .

test that this works:
docker run -e PORT=8000 -p 9090:8000 your_image_name
