var path = require("path");
// var webpack = require('webpack');
var BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CopyPlugin = require("copy-webpack-plugin");
const BrowserSyncPlugin = require("browser-sync-webpack-plugin");
const PurgecssPlugin = require("purgecss-webpack-plugin");

module.exports = {
    context: __dirname,
    entry: ["./static/src/js/app.js", "./static/src/main.css"],
    output: {
        path: path.resolve("./static/local/"),
        filename: "[name]-[hash].js",
    },
    devtool: "source-map",
    devServer: {
        contentBase: path.join(__dirname, "/"),
        compress: true,
        port: 9000,
    },
    module: {
        rules: [
            {
                test: /\.m?js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env"],
                    },
                },
            },
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                        options: {
                            sourceMap: true,
                            hmr: process.env.NODE_ENV === "development",
                        },
                    },
                    {
                        loader: "css-loader",
                        options: {
                            sourceMap: true,
                        },
                    },
                    {
                        loader: "postcss-loader",
                        options: {
                            sourceMap: true,
                            postcssOptions: {
                                plugins: [
                                    require("tailwindcss"),
                                    require("autoprefixer"),
                                ]
                            }
                        },
                    }
                ],
            },
            {
                test: /\.js$/,
                use: ["source-map-loader"],
                enforce: "pre",
            }
        ],
    },
    plugins: [
        new BundleTracker({
            filename: "./webpack-stats.json",
        }),
        new MiniCssExtractPlugin({
            filename: "[name].[hash].css",
            chunkFilename: "[id].[hash].css",
            ignoreOrder: false,
        })
    ],
};
