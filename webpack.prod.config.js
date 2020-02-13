var config = require('./webpack.config.js');
var BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CopyPlugin = require('copy-webpack-plugin');

config.output.path = require('path').resolve('./static/dist');

config.plugins = [
    new BundleTracker({
        filename: './webpack-stats-prod.json'
    }),
    new MiniCssExtractPlugin({
        filename: '[name].[hash].css',
        chunkFilename: '[id].[hash].css',
        ignoreOrder: false
    }),
    new CopyPlugin([{
        from: './static/src/js/libs/**/*',
        to: './js/libs/[name].[ext]'
    }, ]),
]

// override any other settings here like using Uglify or other things that make sense for production environments.

module.exports = config;