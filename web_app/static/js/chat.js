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
      let data = JSON.parse(event.data);
      document.getElementById('inbox').innerHTML = event.data;
      refresh(JSON.parse(event.data));
    }
    socket.onopen = function(event) {
      socket.send("Alive...");
      var ping = setInterval(function () {
        if(socket.readyState === WebSocket.OPEN) {
          socket.send("Alive...");
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
      let [added, changed, removed] = reconstructPacket(load[key]);
      data[key] = data[key].concat(added);
      data[key] = data[key].filter(obj => !removed.has(obj.name));
      data[key].map(obj => { changed[obj.name]? (obj.size = changed[obj.name]): null; });
      data[key].sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()));
    }
    inbox.empty();
    for(var key in load) {
      for(let i = 0; i < data[key].length; i++){
        inbox.append(`<li><a href="${ data[key][i].url }">${ data[key][i].name }</a>: ${ data[key][i].size }</li>`);
      }
    }
  };

  var reconstructPacket = function (data) {
    let added = [];
    let removed = new Set();
    let changed = {};
    let switchCase = {
      "1": (v) => { added.push(v); },
      "0": (v) => { changed[v.name] = v.size; },
      "-1": (v) => { removed.add(v.name); }
    }
    for(let tuple of data) {
      tuple[2]['name'] = tuple[0];
      switchCase[`${ tuple[1] }`](tuple[2]);
    }
    return [added, changed, removed];
  }

  return {
    connect: connect
  };
}

$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    WebSocketHandler().connect();
});
