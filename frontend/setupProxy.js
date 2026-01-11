const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  // Only proxy API endpoints, silently handle errors for offline backend
  const apiProxy = createProxyMiddleware({
    target: 'http://localhost:8000',
    changeOrigin: true,
    logLevel: 'silent',
    ws: false, // Disable websocket proxying
    onError: (err, req, res) => {
      // Silently handle proxy errors - backend is just offline
      // Don't log errors for favicon, hot-update, etc.
      if (!req.path.includes('favicon') && !req.path.includes('hot-update')) {
        // Errors are handled in the React app, no need to log here
      }
    },
    onProxyReq: () => {
      // Silent - no logging
    }
  });

  // Only proxy specific API endpoints
  app.use('/api', apiProxy);
  app.use('/demo', apiProxy);
  app.use('/predict', apiProxy);
  app.use('/health', apiProxy);
  
  // All other requests (favicon, hot-update, etc.) are NOT proxied
  // This prevents ECONNREFUSED errors for non-API requests
};
