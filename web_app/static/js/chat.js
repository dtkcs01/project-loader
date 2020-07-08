function WebSocketHandler() {
  var socket = null;
  var pathBuilder = PathBuilder();
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
