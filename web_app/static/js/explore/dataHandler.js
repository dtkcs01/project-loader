/*
  Modules required:
    1. HTMLBuilder [ htmlBuilder.js ]
  Contents:
    1. function [ DataHandler ]
*/
function DataHandler(pathBuilder) {
  /*
    Structure:
      1. Declarations [ 4 ]
      2. Functions [ 2 private 1 public ]
        i. function [ reconstructPacket ] ( private )
        ii. function [ renderData ] ( private )
        iii. function [ refresh ] ( public )
      3. function call [ function [ htmlBuilder.constructLocationForWindow ] ]
      3. Return
  */

  var parent = {
    name: '..',
    type: 'folder',
    url: pathBuilder.buildURL(pathBuilder.getParentPath())
  };
  var data = {
    folders: [],
    files: []
  };
  var filterData = {
    'all': () => ['All', [...data.folders, ...data.files]],
    'folders': () => ['Folders', [...data.folders]],
    'files': () => ['Files', [...data.files]]
  };
  var htmlBuilder = HTMLBuilder(pathBuilder);

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
    let renderData = filterData[document.querySelector('select[name=filter]').value]()[1];
    for(let i = 0; i < renderData.length; i++){
      contents.append(htmlBuilder.constructRowItem(renderData[i]));
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

  htmlBuilder.constructHeader(filterData, renderData);

  return {
    refresh: refresh
  };
}
