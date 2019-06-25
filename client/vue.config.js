var webpack = require("webpack");

module.exports = {
  devServer: {
    port: process.env.PORT,
    public: process.env.PUBLIC_ADDRESS,
    disableHostCheck: true,
    proxy: {
      "/api": {
        target: process.env.API_PROXY,
        secure: false
      }
    }
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

    config.module
      .rule("txt")
      .test(/\.txt$/i)
      .use()
      .loader("raw-loader");
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
