var PubNub = require('pubnub');
var express = require('express');

var requestTime = function (req, res, next) {
  req.requestTime = Date.now();
  console.log(req.requestTime);
  next();
}