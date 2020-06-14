function buildHTML(element, data, contents) {
  element = $(document.createElement(element));
  (data? () => { for(let key in data) { element.attr(key, data[key]); } }: () => {})();
  (contents? () => { for(let content of contents){ content? element.append(content): null; } }: () => {})();
  return element;
}

function WebSocketHandler() {
  var socket = null;
  var data = { folders: [], files: [] };
  var parent = null;

  var connect = function() {
    let pathArray = window.location.pathname.split('/')
                  .filter(name => (name.trim().length > 0))
                  .slice(1, );
    let path = pathArray.join('/');
    parent = { name: '..', type: 'folder', url: `/d/${ pathArray.slice(0, pathArray.length - 1).join('/') }`};
    let url = `ws://${ window.location.host }/websocket/${ path }`;
    socket = new WebSocket(url);
    socket.onmessage = function(event) {
      let data = JSON.parse(event.data);
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
    constructLocation(pathArray);
  };

  var redirect = function(url) {
    url = `${ window.location.protocol }//${ window.location.host }${ url }`;
    $(window.location).attr('href', url);
  }

  var constructSwitchMode = function (url) {
    let outer = buildHTML('div', { 'class': 'switch-mode' });
    let ball = buildHTML('div', { 'class': 'ball bg-primary' });
    outer.append(ball);
    outer.click(function() {
      ball.prop('classList').remove('bg-primary');
      ball.prop('classList').add('bg-danger');
      var left = 2;
      var int = setInterval(function (){
        ball.css('left', `${left}px`);
        ((left < 26)? () => { left += 1; }: () => { clearInterval(int); redirect(url);})();
      }, 5);
    });
    return outer;
  };

  var constructLocation = function(pathArray) {
    let location = $(document.getElementById('location'));
    let link = '';
    for(let dir of pathArray) {
      link += `/${ dir }`;
      location.append($(`<a href="/d${ link }">${ dir }</a>`));
      location.append(' / ');
    }
    let mode = $(document.getElementById('toggle-mode'));
    mode.append('Explore ');
    mode.append(constructSwitchMode(`/a${ link }`));
    mode.append(' Analyse');
  };

  var constructCheckBox = function(name) {
    let container = buildHTML('div', { 'class': 'custom-control custom-checkbox' });
    container.append(buildHTML('input', {
      'type': 'checkbox',
      'class': 'custom-control-input',
      'id': name,
      'name': name
    }));
    container.append(buildHTML('label', {
      'class': 'custom-control-label',
      'for': name
    }));
    return container;
  };

  var constructOptions = function(url, size) {
    let container = buildHTML(
      'div',
      { 'class': 'float-right' },
      [
        size? buildHTML('div', { 'class': 'text-muted small' }, [size]): null,
        buildHTML(
          'a',
          { 'href': `${ url }?action=rename` },
          [buildHTML('button', { 'class':  'btn btn-rename btn-sm'}, ['Rename'])]
        ),
        buildHTML(
          'a',
          { 'href': `${ url }?action=delete` },
          [buildHTML('button', { 'class':  'btn btn-danger btn-sm'}, [buildHTML('i', { 'class': 'fa fa-trash' })])]
        )
      ]
    );
    return container;
  };

  var constructDataRow = function(rowData) {
    let isParent = !(rowData.name.localeCompare('..') == 0);
    let container = buildHTML('div', null, [
      buildHTML('div', { 'class': 'row' }, [
        buildHTML('div', { 'class': 'col-12 py-1' }, [
          isParent? constructCheckBox(rowData.name): null,
          buildHTML('a', { 'href': rowData.url }, [
            buildHTML('i', { 'class': `fa fa-${ rowData.type }-o` }),
            ` ${ rowData.name }`
          ]),
          isParent? constructOptions(rowData.url, rowData.size): null
        ])
      ]),
      buildHTML('div', { 'class': 'row' }, [buildHTML('hr', { 'class': 'tab-sep' })])
    ]);
    return container;
  };

  var refresh = function(load) {
    let contents = $(document.getElementById('contents'));
    for(var key in load) {
      let [added, changed, removed] = reconstructPacket(load[key]);
      data[key] = data[key].concat(added);
      data[key] = data[key].filter(obj => !removed.has(obj.name));
      data[key].map(obj => { changed[obj.name]? (obj.size = changed[obj.name]): null; });
      data[key].sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()));
    }
    contents.empty();
    contents.append(constructDataRow(parent));
    for(var key in load) {
      for(let i = 0; i < data[key].length; i++){
        contents.append(constructDataRow(data[key][i]));
      }
    }
  };

  var reconstructPacket = function(data) {
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
