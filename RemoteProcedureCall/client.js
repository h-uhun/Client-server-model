const net = require('node:net');
const data = require('./config.json');

process.stdin.setEncoding('utf-8');
process.stdin.resume();

const METHOD_CONFIG = {
  "floor": 1,
  "nroot": 2,
  "reverse": 1,
  "validAnagram": 2,
}

// connection with the server (not a request)
// As createConnection is asynchronous
const client = net.createConnection({ path: data.filepath }, () => {
  console.log('connected to server!');

  process.stdin.on('data', (input) => {
    const message = input.trim();
    if(message === 'exit') {
      client.end();
      process.exit();
    }

    function exitSTDIN() {
      console.log("The command is incorrect.");
      return;
    }

    // Should validation be performed on both the client and server? (like a forms)
    // Forntend : improving the user experience?
    // Backend : Checking for invalid data?

    const [method, ...params] = message.split(" ");
    
    if(!method || params.length === 0) {
      console.log("The command is incorrect.");
      return;
    }

    const paramsLength = METHOD_CONFIG[method];

    if(method !== "sort") {
      if(paramsLength === undefined) {
        console.log(`Error: Unknown method "${method}".`);
        return;
      }
      if(params.length !== paramsLength) {
        console.log(`Error: Method "${method}" requires ${paramsLength} parameter.`);
        return;
      }
    }

    dataToSend = {
      "method" : method,
      "params" : params,
      "param_types" : typeof params[0],
      "id" : crypto.randomUUID()
    }
    const jsonString = JSON.stringify(dataToSend);

    // send the request
    client.write(jsonString + '\n');
  });
});

client.on('data', (data) => {
  console.log(data.toString().trim());
});