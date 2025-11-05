const net = require('node:net');
const data = require('./config.json')

// connection with the server (not a request)
const client = net.createConnection({ path: data.filepath}, () => {
  console.log('connected to server!');
});

