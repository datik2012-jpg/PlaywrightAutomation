const http = require('node:http');
const { readFile } = require('node:fs');
const { join } = require('node:path');

const port = Number(process.env.PORT || 3000);
const pages = new Map([
  ['/', 'index.html'],
  ['/index.html', 'index.html'],
  ['/courts.html', 'courts.html'],
  ['/api-login.html', 'api-login.html'],
]);

const demoUser = {
  email: 'dani@example.com',
  password: '1234567',
};

const apiToken = 'demo-api-token';
const courts = [
  { id: 1, name: 'Court A', status: 'Available', time: '18:00' },
  { id: 2, name: 'Court B', status: 'Available', time: '18:00' },
];

function sendJson(response, status, body) {
  response.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  response.end(JSON.stringify(body));
}

function handleLoginApi(request, response) {
  if (request.method !== 'POST') {
    response.writeHead(405, {
      Allow: 'POST',
      'Content-Type': 'application/json; charset=utf-8',
    });
    response.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }

  let body = '';

  request.on('data', (chunk) => {
    body += chunk;

    if (body.length > 10_000) {
      request.destroy();
    }
  });

  request.on('end', () => {
    let credentials;

    try {
      credentials = JSON.parse(body);
    } catch {
      sendJson(response, 400, { error: 'Request body must be valid JSON' });
      return;
    }

    if (!credentials.email || !credentials.password) {
      sendJson(response, 400, { error: 'Email and password are required' });
      return;
    }

    if (
      credentials.email !== demoUser.email ||
      credentials.password !== demoUser.password
    ) {
      sendJson(response, 401, { error: 'Invalid email or password' });
      return;
    }

    sendJson(response, 200, {
      success: true,
      token: apiToken,
      user: { email: demoUser.email },
    });
  });
}

function handleCourtsApi(request, response) {
  if (request.method !== 'GET') {
    response.writeHead(405, {
      Allow: 'GET',
      'Content-Type': 'application/json; charset=utf-8',
    });
    response.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }

  if (request.headers.authorization !== `Bearer ${apiToken}`) {
    sendJson(response, 401, { error: 'Unauthorized' });
    return;
  }

  sendJson(response, 200, {
    success: true,
    courts,
  });
}

const server = http.createServer((request, response) => {
  const pathname = new URL(request.url, `http://${request.headers.host}`).pathname;

  if (pathname === '/api/login') {
    handleLoginApi(request, response);
    return;
  }

  if (pathname === '/api/courts') {
    handleCourtsApi(request, response);
    return;
  }

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
