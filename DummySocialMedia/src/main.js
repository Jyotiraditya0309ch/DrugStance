/**
 * @author Faiyaz Shaikh <www.shtakkar@gmail.com>
 * GitHub repo: https://github.com/yTakkar/React-Instagram-Clone-2.0
 */
const http = require('http');
const url = require('url');

// Define the port
const PORT = process.env.PORT || 8000;

// Create the server
const server = http.createServer((req, res) => {
    // Only handle POST requests
    if (req.method === 'POST' && req.url === 'http://localhost:8000/api/post-it') {
        let body = '';

        // Collect the data
        req.on('data', chunk => {
            body += chunk.toString(); // Convert Buffer to string
        });

        req.on('end', () => {
            const userIp = req.socket.remoteAddress; // Get the user's IP address
            const { content } = JSON.parse(body); // Parse the JSON body

            // Log or save the user's IP address and the content
            console.log(`Received post from ${userIp}: ${content}`);

            // Respond back to the user
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ message: 'Post received', userIp }));
        });
    } else {
        // Handle other routes
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
    }
});

// Start the server
server.listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running on http://0.0.0.0:${PORT}`);
});

// FOR LOGGEDIN USER
import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import store from './store/store'
import App from './components/App'

let element = document.getElementById('root')
if (element) {
  ReactDOM.render(
    <Provider store={store}>
      <App />
    </Provider>,
    element
  )
} else {
  // USER SYSTEM (FOR NOT-LOGGEDIN USER)
  require('./user-system/user-system')
}
