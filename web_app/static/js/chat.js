/*
  Modules required:
    1. PathBuilder [ pathBuilder.js ]
    2. DataHandler [ dataHandler.js ]
  Contents:
    1. function [ WebSocketHandler ]
    2. Entry point [ $(document).ready ]
*/

function WebSocketHandler() {
  /*
    Structure:
      1. Declarations [ 3 ]
      2. Functions [ 2 private 1 public ]
        i. function [ onMessageReceive ] ( private )
        ii. function [ onSocketConnection ] ( private )
        iii. function [ connect ] ( public )
      3. Return
  */

  var socket = null;
  var pathBuilder = PathBuilder(); // Shared between all modules
  var dataHandler = DataHandler(pathBuilder);

  var onMessageReceive = function(event) {
    let data = JSON.parse(event.data);
    dataHandler.refresh(JSON.parse(event.data));
  };

  var onSocketConnection = function(event) {
    socket.send("Alive...");
    var ping = setInterval(function () {
      if(socket.readyState === WebSocket.OPEN) {
        socket.send("Alive...");
      } else {
        alert('Lost Connection to server...');
        clearInterval(ping);
      }
    }, 2000);
  };

  var connect = function() {
    let url = `ws://${ window.location.host }/websocket/${ pathBuilder.getPath() }`;
    socket = new WebSocket(url);
    socket.onmessage = onMessageReceive;
    socket.onopen = onSocketConnection;
  };

  return {
    connect: connect
  };
}

$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    WebSocketHandler().connect();
});
