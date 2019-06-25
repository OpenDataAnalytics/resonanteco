var webpack = require("webpack");

module.exports = {
  devServer: {
    port: 8081,
    public: process.env.PUBLIC_ADDRESS,
    disableHostCheck: true
  },
  publicPath: process.env.VUE_APP_STATIC_PATH,
  chainWebpack: config => {
    config.module
      .rule("additional")
      .test(/\.m?jsx?$/)
      .include.add(/@girder\/components/)
      .add(/vue-utilities/)
      .end()
      .use()
      .loader("babel-loader");
  },
  configureWebpack: () => {
    return {
      plugins: [
        new webpack.DefinePlugin({
          "process.env": {
            VERSION: JSON.stringify(require("./package.json").version)
          }
        })
      ]
    };
  }
};
