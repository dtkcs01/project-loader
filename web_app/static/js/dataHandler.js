function DataHandler(pathBuilder) {
  var parent = {
    name: '..',
    type: 'folder',
    url: pathBuilder.buildURL(pathBuilder.getParentPath())
  };
  var data = {
    folders: [],
    files: []
  };

  var htmlBuilder = HTMLBuilder(pathBuilder);
  htmlBuilder.constructLocationForWindow(pathBuilder.getPath().split('/'));

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
  };

  var renderData = function() {
    let contents = $(document.getElementById('contents'));
    contents.empty();

    contents.append(htmlBuilder.constructRowItem(parent));
    for(var key in data) {
      for(let i = 0; i < data[key].length; i++){
        contents.append(htmlBuilder.constructRowItem(data[key][i]));
      }
    }
  };

  var refresh = function(load) {
    for(var key in load) {
      let [added, changed, removed] = reconstructPacket(load[key]);
      data[key] = data[key].concat(added);
      data[key] = data[key].filter(obj => !removed.has(obj.name));
      data[key].map(obj => { changed[obj.name]? (obj.size = changed[obj.name]): null; });
      data[key].sort((a, b) => a.name.toLowerCase().localeCompare(b.name.toLowerCase()));
    }
    renderData();
  };

  return {
    refresh: refresh
  };
}