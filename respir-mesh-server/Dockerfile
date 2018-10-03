# FROM golang:1.9.6
# FROM golang:1.11-alpine
FROM golang:1.11

# https://hub.docker.com/r/library/golang/tags/

# run ls
# run ls /RespirMeshServer

RUN go get github.com/golang/protobuf/protoc-gen-go && go get github.com/gorilla/websocket

CMD cd /RespirMeshServer/ServerGo/src && go run /RespirMeshServer/ServerGo/src/init.go