const config = require('./webpack.config.js');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
// const CopyPlugin = require('copy-webpack-plugin');
// const path = require('path')
const glob = require('glob')
const PurgecssPlugin = require("purgecss-webpack-plugin");

config.output.path = require('path').resolve('./static/dist');

config.plugins = [
    new BundleTracker({
        filename: './webpack-stats-prod.json'
    }),
    new PurgecssPlugin({
        paths: glob.sync(`templates/**/*`, {
            nodir: true
        })
    }),
    new MiniCssExtractPlugin({
        filename: '[name].[hash].css',
        chunkFilename: '[id].[hash].css',
        ignoreOrder: false
    }),
    // new CopyPlugin([{
    //     from: './static/src/libs/**/*',
    //     to: './libs/[name].[ext]'
    // }, ]),
]

// override any other settings here like using Uglify or other things that make sense for production environments.

module.exports = config;
