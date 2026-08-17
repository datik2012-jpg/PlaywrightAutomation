const http = require('node:http');
const { readFile } = require('node:fs');
const { join } = require('node:path');

const port = Number(process.env.PORT || 3000);
const pages = new Map([
  ['/', 'index.html'],
  ['/index.html', 'index.html'],
  ['/courts.html', 'courts.html'],
]);

const server = http.createServer((request, response) => {
  const pathname = new URL(request.url, `http://${request.headers.host}`).pathname;
  const fileName = pages.get(pathname);

  if (!fileName) {
    response.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    response.end('Not found');
    return;
  }

  const pagePath = join(__dirname, 'app', fileName);
  readFile(pagePath, (error, page) => {
    if (error) {
      response.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
      response.end('Unable to load the page');
      return;
    }

    response.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    response.end(page);
  });
});

server.listen(port, '127.0.0.1', () => {
  console.log(`Login demo available at http://127.0.0.1:${port}`);
});
