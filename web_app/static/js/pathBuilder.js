var PathBuilder = function() {
  var mode = null;
  var path = null;
  var parentPath = null;

  var buildPaths = function() {
    let tmp = window.location.pathname.split('/');
    tmp = tmp.filter(name => name.trim().length > 0);
    // parent scope variables
    mode = tmp[0];
    path = tmp.slice(1, ).join('/');
    parentPath = tmp.slice(1, tmp.length-1).join('/');
  }

  var getMode = function() { return mode; };

  var getPath = function() { return path; };

  var buildURL = function(inPath, viaMode) {
    return `/${ viaMode || mode }/${ inPath === undefined? path: inPath }`;
  };

  var getParentPath = function() { return parentPath; };

  var switchModes = {
    'a': 'd',
    'd': 'a'
  };

  buildPaths();

  return {
    getMode: getMode,
    getPath: getPath,
    buildURL: buildURL,
    switchModes: switchModes,
    getParentPath: getParentPath
  };
}
