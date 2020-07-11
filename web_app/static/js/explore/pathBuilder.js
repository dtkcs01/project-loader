/*
  Contents:
    1. function [ PathBuilder ]
*/
var PathBuilder = function() {
  /*
    Structure:
      1. Declarations [ 4 ]
      2. Functions [ 1 private 5 public ]
        i. function [ buildPaths ] ( private )
        ii. function [ getMode ] ( public )
        iii. function [ getPath ] ( public )
        iv. function [ buildURL ] ( public )
        v. function [ getParentPath ] ( public )
        vi. function [ switchMode ] ( public )
      3. function call [ function [ buildPaths ] ]
      4. Return
  */

  var mode = null;
  var path = null;
  var parentPath = null;
  var switchModes = {
    'a': 'd',
    'd': 'a'
  };

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

  var switchMode = function() { return switchModes[mode]; }

  buildPaths();

  return {
    getMode: getMode,
    getPath: getPath,
    buildURL: buildURL,
    switchMode: switchMode,
    getParentPath: getParentPath
  };
}
