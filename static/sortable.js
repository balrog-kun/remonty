function make_sortable_elem(elem, col) {
  var up = document.createElement('a');
  var down = document.createElement('a');

  up.setAttribute('class', 'sort-up');
  down.setAttribute('class', 'sort-down');

  up.setAttribute('href', url_template.replace('__placeholder', '-' + col));
  down.setAttribute('href', url_template.replace('__placeholder', '' + col));

  elem.appendChild(down);
  elem.appendChild(up);
}

function make_sortable() {
  var els = document.getElementsByTagName('td');

  for (i = 0; i < els.length; i++)
    if (els[i].hasAttribute('sort-col'))
      make_sortable_elem(els[i], els[i].getAttribute('sort-col'));
}
