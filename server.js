#!/usr/bin/env node
const http = require('http');
const express = require('express');
const bodyParser = require('body-parser');
const { createBundleRenderer, createRenderer } = require('vue-server-renderer');

const ADDRESS = '127.0.0.1';
const PORT = 9009;

const app = express();
const server = http.Server(app);
const rendererMap = new Map();

app.use(bodyParser.json());

app.get('/', function(req, res) {
  res.end('Vue render server');
});

app.post('/render', (req, res) => {
  const body = req.body;
  const props = body.serializedProps ? JSON.parse(body.serializedProps) : null;
  let renderer = rendererMap.get(body.path);
  if (!renderer) {
    if (props.clientManifest) {
      const clientManifest = require(props.clientManifest);
      renderer = createBundleRenderer(body.path, {
        runInNewContext: false,
        clientManifest,
      });
    } else {
      renderer = createRenderer({
        runInNewContext,
      });
    }
    rendererMap.set(body.path, renderer);
  }
  const context = props.context || {};
  renderer.renderToString(context, (err, markup) => {
    if (err) {
      res.json({
        error: {
          type: err.constructor.name,
          message: err.message,
          stack: err.stack
        },
        markup: null,
      });
    } else {
      const outContext = Object.assign({}, context);
      outContext.markup = markup;
      outContext.styles = context.styles;
      outContext.state = context.renderState();
      delete outContext._styles;
      res.json({
        error: null,
        markup: outContext,
      });
    }
  });
});

server.listen(PORT, ADDRESS, () => {
  console.log('Vue render server listening at http://' + ADDRESS + ':' + PORT);
});
