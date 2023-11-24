const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  // 로컬 서버로의 요청을 프록시합니다.
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://127.0.0.1:5000',
      changeOrigin: true
    })
  );

  // Cloudtype 서버로의 요청을 프록시합니다.
  app.use(
    '/cloudapi',
    createProxyMiddleware({
      target: 'https://port-0-realpuppypalapi-3szcb0g2blpawubnm.sel5.cloudtype.app',
      changeOrigin: true,
      pathRewrite: { '^/cloudapi': '/api' }, // '/cloudapi' 경로를 제거합니다.
    })
  );
};
