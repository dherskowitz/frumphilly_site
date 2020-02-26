var path = require('path');
// var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CopyPlugin = require('copy-webpack-plugin');
const BrowserSyncPlugin = require('browser-sync-webpack-plugin')

module.exports = {
    context: __dirname,
    entry: ["./static/src/js/app.js", "./static/src/scss/app.scss"],
    output: {
        path: path.resolve("./static/local/"),
        filename: "[name]-[hash].js"
    },
    devtool: "source-map",
    devServer: {
        contentBase: path.join(__dirname, "/"),
        compress: true,
        port: 9000
    },
    module: {
        rules: [{
                test: /\.m?js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env"]
                    }
                }
            },
            {
                test: /\.(sa|sc|c)ss$/,
                use: [{
                        loader: MiniCssExtractPlugin.loader,
                        options: {
                            sourceMap: true,
                            hmr: process.env.NODE_ENV === "development"
                        }
                    },
                    {
                        loader: "css-loader",
                        options: {
                            sourceMap: true
                        }
                    },
                    {
                        loader: "postcss-loader",
                        options: {
                            ident: "postcss",
                            sourceMap: true,
                            plugins: [require("autoprefixer")]
                        }
                    },
                    {
                        loader: "sass-loader",
                        options: {
                            sourceMap: true
                        }
                    },
                ]
            },
            {
                test: /\.js$/,
                use: ["source-map-loader"],
                enforce: "pre",
            },
            {
                test: /\.(gif|png|jpe?g|svg)$/i,
                use: [
                    'file-loader',
                    {
                        loader: 'image-webpack-loader',
                        options: {
                            mozjpeg: {
                                progressive: true,
                                quality: 65
                            },
                            optipng: {
                                enabled: false,
                            },
                            pngquant: {
                                quality: '65-90',
                                speed: 4
                            },
                            bypassOnDebug: true, // webpack@1.x
                            disable: true, // webpack@2.x and newer
                        },
                    },
                ],
            }
        ]
    },
    plugins: [
        new BundleTracker({
            filename: './webpack-stats.json'
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
        new BrowserSyncPlugin({
            host: 'localhost',
            port: 3000,
            proxy: 'http://192.168.99.100:8001/'
        })
    ]
}