const express = require('express');
const https = require('https');
const fs = require('fs');
const path = require('path');
const compression = require('compression');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;
const sslKeyPath = process.env.SSL_KEY_PATH ;

const sslCertPath = process.env.SSL_CERT_PATH ;

// Use compression middleware
app.use(compression());

// Serve static files from the 'build' folder
app.use(express.static(path.join(__dirname, 'build')));

// Handle other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});


// HTTPS options
const options = {
  key: fs.readFileSync(sslKeyPath),
  cert: fs.readFileSync(sslCertPath),
};

// Create an HTTPS server
const server = https.createServer(options, app);

// Start the server
server.listen(port, () => {
  console.log(`Server running at https://localhost:${port}`);
});