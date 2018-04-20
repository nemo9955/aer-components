FROM golang:1.8

# run ls
# run ls /RespirMeshServer
RUN go get github.com/golang/protobuf/protoc-gen-go

CMD cd /RespirMeshServer/ServerGo/src && go run /RespirMeshServer/ServerGo/src/init.go