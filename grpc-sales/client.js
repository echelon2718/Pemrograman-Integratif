const grpc = require("@grpc/grpc-js");
var protoLoader = require("@grpc/proto-loader");

const PROTO_PATH = "./sales.proto";

const options = {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
};

var packageDefinition = protoLoader.loadSync(PROTO_PATH, options);
const salesProto = grpc.loadPackageDefinition(packageDefinition);
const client = new salesProto.productService(
  "127.0.0.1:50051",
  grpc.credentials.createInsecure()
);

client.getAll({}, (error, products) => {
  if (error) {
    console.error(error);
    return;
  }
  console.log(products);
});
