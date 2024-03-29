const config = require("./webpack.config.js");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const path = require("path");
// const glob = require("glob");
// const PurgecssPlugin = require("purgecss-webpack-plugin");
const purgecss = require("@fullhuman/postcss-purgecss");
const cssnano = require("cssnano");

module.exports = {
    entry: ["./static/src/js/app.js", "./static/src/main.css"],
    // optimization: {
    //     minimizer: [
    //         // new TerserPlugin({
    //         //     sourceMap: true,
    //         // }),
    //         // new OptimizeCSSAssetsPlugin({
    //         //     sourceMap: true,
    //         // }),
    //     ],
    // },
    output: {
        path: path.resolve(__dirname, "static/dist"),
        filename: "[name]-[hash].js",
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                        options: {
                            sourceMap: true,
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
                            postcssOptions: {
                                plugins: [
                                    require("tailwindcss"),
                                    require("autoprefixer"),
                                    purgecss({
                                        content: ["./templates/**/*.html"],
                                        whitelist: ['trix-editor', 'blockquote', 'textarea', 'bg-green-400',
                                            'bg-yellow-500',
                                            'bg-red-500',],
                                        defaultExtractor: (content) => content.match(/[\w-/:]+(?<!:)/g) || [],
                                    }),
                                    cssnano({
                                        preset: "default",
                                    }),
                                ],
                            }
                        },
                    },
                ],
            },
        ],
    },
    plugins: [
        new BundleTracker({
            filename: "./webpack-stats-prod.json",
        }),
        // new PurgecssPlugin({
        //     paths: glob.sync(`templates/**/*`, {
        //         nodir: true,
        //     }),
        // }),
        new MiniCssExtractPlugin({
            filename: "[name].[hash].css",
            chunkFilename: "[id].[hash].css",
            ignoreOrder: false,
        }),
    ],
};
