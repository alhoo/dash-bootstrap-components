'use strict';

var path = require('path');
var webpack = require('webpack');

var OccurrenceOrderPlugin = require('webpack').optimize.OccurrenceOrderPlugin;

var ROOT = process.cwd();
var SRC = path.join(ROOT, 'src');
var DEMO = path.join(ROOT, 'demo');

var NODE_ENV = process.env.NODE_ENV || 'development';
var environment = JSON.stringify(NODE_ENV);

var LIBRARY_NAME = 'dash-bootstrap-components';
var BUILD_PATH = path.join(ROOT, LIBRARY_NAME, '_components');

/* eslint-disable no-console */
console.log('Current environment: ' + environment);
/* eslint-enable no-console */

module.exports = {
  cache: false,
  context: SRC,
  mode: NODE_ENV,
  externals: [
    {
      react: {
        root: 'React',
        commonjs2: 'react',
        commonjs: 'react',
        amd: 'react'
      }
    },
    {
      'react-dom': {
        root: 'ReactDOM',
        commonjs2: 'react-dom',
        commonjs: 'react-dom',
        amd: 'react-dom'
      }
    }
  ],
  module: {
    noParse: /node_modules\/json-schema\/lib\/validate\.js/, // used to get `request` to work: https://github.com/request/request/issues/1920#issuecomment-171246043
    rules: [
      {
        test: /\.json$/,
        loader: 'json-loader'
      },
      {
        test: /\.jsx?$/,
        include: [SRC, DEMO],
        /*
         * Use require.resolve to get a deterministic path
         * and avoid webpack's magick loader resolution
         */
        use: [
          {
            loader: 'babel-loader'
          }
        ]
      },
      {
        test: /\.css$/,
        use: [
          {
            loader: 'style-loader'
          },
          {
            loader: 'css-loader'
          }
        ]
      }
    ]
  },
  plugins: [new OccurrenceOrderPlugin(true)],
  optimization: {
    minimize: true
  },
  entry: {
    main: './index.js'
  },
  output: {
    library: LIBRARY_NAME,
    libraryTarget: 'umd',
    path: path.join(ROOT, 'lib/'),
    filename: LIBRARY_NAME + '.min.js',
    umdNamedDefine: true
  }
};
