const http = require('http');
const express = require('express');
const bodyParser = require('body-parser');

var ADDRESS = '127.0.0.1';
var PORT = 9009;

const app = express();
const server = http.Server(app);

app.use(bodyParser.json());

app.post('/render', (req, res) => {
  res.json({
    error: null,
    markup: req.body,
  });
});

server.listen(PORT, ADDRESS, () => {
  console.log(`Render server listening at http://${ADDRESS}:${PORT}`);
});
