function webSocketHandler(web_config) {
  var socket = new WebSocket(`ws://${ web_config.ip }:${ web_config.port }/`);
  var config_string = JSON.stringify(web_config);
  var p = document.getElementById('is_alive');

  var pingToServer = function() {
    socket.onopen = function() {
      socket.send(config_string);
      var pingModule = setInterval(function() {
        if(socket.readyState === socket.OPEN) {
          socket.send(config_string);
        } else {
          clearInterval(pingModule);
          alert('Connection lost with server!!');
        }
      }, web_config.ping_interval);
    }
  };

  var listenToServer = function() {
    socket.onmessage = function (event) {
        p.innerHTML = event.data;
    };
  };

  var init = function() {
    pingToServer();
    listenToServer();
  }

  return {
    init: init
  };
}
