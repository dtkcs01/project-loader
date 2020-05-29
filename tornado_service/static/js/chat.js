function WebSocketHandler() {
  var socket = null;
  var data = { folders : [], files: [] };

  var connect = function() {
    let path = window.location.pathname.split('/')
                  .filter(name => (name.trim().length > 0))
                  .slice(1, )
                  .join('/');
    let url = `ws://${ window.location.host }/websocket/${ path }`;
    socket = new WebSocket(url);
    socket.onmessage = function(event) {
      refresh(JSON.parse(event.data));
    }
    socket.onopen = function(event) {
      socket.send(JSON.stringify({'id':'some'}));
      var ping = setInterval(function () {
        if(socket.readyState === WebSocket.OPEN) {
          socket.send(JSON.stringify({'id' : 'some'}));
        } else {
          alert('Lost Connection to server...');
          clearInterval(ping);
        }
      }, 2000);
    }
  };

  var refresh = function(load) {
    let inbox = $('#inbox');
    for(var key in load) {
      let added = load[key]
                    .filter(obj => obj[1])
                    .map(obj => obj[0]);
      let removed = new Set(load[key]
                    .filter(obj => !obj[1])
                    .map(obj => obj[0]));
      data[key] = data[key].concat(added);
      data[key] = data[key].filter(name => !removed.has(name));
      data[key].sort((a, b) => { return a.toLowerCase().localeCompare(b.toLowerCase()) });
    }
    inbox.empty();
    for(let i = 0; i < data.folders.length; i++){
      inbox.append(`<li>${ data.folders[i] }</li>`);
    }
    for(let i = 0; i < data.files.length; i++){
      inbox.append(`<li><b>${ data.files[i] }</b></li>`);
    }
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
