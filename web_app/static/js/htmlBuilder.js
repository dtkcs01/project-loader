var HTMLBuilder = function(pathBuilder) {
  var buildHTML = function(tag, attributes, children) {
    var setAttributes = function(element, attributes) {
      for(let key in attributes) {
        element.attr(key, attributes[key]);
      }
    };

    var appendChildren = function appendChild(element, children) {
      for(let child in children) {
        children[child]? element.append(children[child]): null;
      }
    };

    let element = $(document.createElement(tag));
    attributes? setAttributes(element, attributes): null;
    children? appendChildren(element, children): null;
    return element;
  }

  var constructToggleModeButton = function() {
    let mode = $(document.getElementById('toggle-mode'));

    mode.append('Explore ');

    let ball = buildHTML('div', {'class': 'ball'});
    let wrapper = buildHTML('div', {'class': 'switch-mode'}, [ball]);
    wrapper.click(() => {
      wrapper.toggleClass('analyse-mode');
      setInterval(function() {
        let path = pathBuilder.buildURL(pathBuilder.getPath(), pathBuilder.switchModes[pathBuilder.getMode()]);
        let url = `${ window.location.protocol }//${ window.location.host }${ path }`;
        $(window.location).attr('href', url);
      }, 300);
    });
    mode.append(wrapper);

    mode.append(' Analyse');
  }

  var constructLocationForWindow = function(pathArray) {
    let location = $(document.getElementById('location'));

    for(let i = 0; i < pathArray.length; i++) {
      location.append(buildHTML('a', {
        'href':pathBuilder.buildURL(pathArray.slice(0, i+1).join('/'))
      }, [decodeURIComponent(pathArray[i])]));
      location.append(' / ');
    }

    constructToggleModeButton();
  }

  var constructOptionForItem = function(url, size) {
    let sizeDisplay = size? buildHTML('div', {'class': 'text-muted small'}, [size]): null;

    let renameButton = buildHTML('button', {'class':  'btn btn-rename btn-sm'}, ['Rename']);
    let renameLink = buildHTML('a', {'href': `${ url }?action=rename`}, [renameButton]);

    let deleteIcon = buildHTML('i', {'class': 'fa fa-trash'});
    let deleteButton = buildHTML('button', {'class':  'btn btn-danger btn-sm'}, [deleteIcon]);
    let deleteLink = buildHTML('a', {'href': `${ url }?action=delete`}, [deleteButton]);

    return buildHTML('div', {'class': 'float-right'}, [sizeDisplay, renameLink, deleteLink]);
  };

  var constructCheckBoxForItem = function(name) {
    let input = buildHTML('input', {
      'type': 'checkbox',
      'class': 'custom-control-input',
      'id': name,
      'name': name
    });

    let label = buildHTML('label', {
      'class': 'custom-control-label',
      'for': name
    });

    return buildHTML('div', { 'class': 'custom-control custom-checkbox' }, [input, label]);
  };

  var constructRowItem = function(data) {
    let isParent = !(data.name.localeCompare('..') == 0);

    let itemIcon = buildHTML('i', { 'class': `fa fa-${ data.type }-o` });
    let itemLink = buildHTML('a', { 'href': data.url }, [itemIcon, ` ${ data.name }`]);
    let checkbox = isParent? constructCheckBoxForItem(data.name): null;
    let options = isParent? constructOptionForItem(data.url, data.size): null;

    let item = buildHTML('div', {'class': 'col-12 py-1'}, [checkbox, itemLink, options]);

    let row = buildHTML('div', { 'class': 'row' }, [item]);
    let separator = buildHTML('div', { 'class': 'row' }, [buildHTML('hr', { 'class': 'tab-sep' })]);

    return buildHTML('div', null, [row, separator]);
  }

  return {
    constructRowItem: constructRowItem,
    constructLocationForWindow: constructLocationForWindow
  };
}
