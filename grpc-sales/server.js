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
const server = new grpc.Server();

let products = [
  {
    id: 1,
    product_name: "Soap",
    brand: "Lux",
    count: 9,
  },
  {
    id: 2,
    product_name: "Ketchup",
    brand: "ABC",
    count: 14,
  },
  {
    id: 3,
    product_name: "Oil",
    brand: "Sunco",
    count: 7,
  },
];

server.addService(salesProto.productService.service, {
  getAll: (_, callback) => {
    callback(null, { product: products });
  },
});

server.bindAsync(
  "127.0.0.1:50051",
  grpc.ServerCredentials.createInsecure(),
  (error, port) => {
    if (error) {
      console.error(error);
      return;
    }
    console.log("Server running at http://127.0.0.1:50051");
    server.start();
  }
);
