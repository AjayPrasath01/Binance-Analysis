const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  console.log({app})
	app.use(
		"/api",
		createProxyMiddleware({
			target: "http://127.0.0.1:8089",
			changeOrigin: true,
            // pathRewrite: {
            //     '^/api': '',
            //   },
		})
	);
};
