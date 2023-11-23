const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api', // 이 경로를 통해 오는 요청은 프록시를 사용합니다.
    createProxyMiddleware({
      target: 'http://127.0.0.1:5000/', // Flask 서버 주소
      changeOrigin: true
    })
  );
};
