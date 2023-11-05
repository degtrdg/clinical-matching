docker build -t degtrdg/clinicalmatching:0.0.7 .
docker push degtrdg/clinicalmatching:0.0.7
https://console.cloud.google.com/run

make a service

port number

For ARM:
docker buildx build --platform linux/amd64 -t {project-name} .
docker buildx build --platform linux/amd64 -t degtrdg/clinicalmatching:0.0.7 .

docker compose up --build
test that this works:
docker run -e PORT=8000 -p 9090:8000 degtrdg/clinicalmatching:0.0.7
