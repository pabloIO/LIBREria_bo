'use strict';
const API = 'http://' + window.location.host + '/api/v1';
let versos;
const poem = document.getElementById('content_poem');

const getPoem = function (){
  $.ajax({
    method: 'GET',
    url: `${API}/poems/page`
  }).done(function(res){
      if(res.success){
	  versos = res.books.slice(-5,);
          displayPoem(versos);
    }else{
      alert('Hubo un problema en la recuperación de datos');
    }
  });
}

const displayPoem = function(versos, status){
    versos.forEach(v => {
	let verso = document.createElement('p');
	verso.textContent = v.verso;
	if (status){
	    verso.classList.add('push')
	}
	if (v.new){
	    verso.classList.add('userVerso')
	}
	poem.appendChild(verso);
    })
}

const updatePoem = function(verso){
    while (poem.firstChild) {
	poem.removeChild(poem.firstChild);
    }
    versos.push({'verso': verso, 'new': 'user'});
    versos = versos.slice(-5,);
    displayPoem(versos, 'push');
}

const uploadPoem = function(verso){
  $.ajax({
    method: 'POST',
    url: `${API}/poems/upload/${verso}`
  }).done(function(res){
    if(res.success){
      updatePoem(verso);
    }else{
      alert('Hubo un problema');
    }
  });
}

const nuevoVerso = function() {
    document.getElementById('newVerso')
	.addEventListener('submit', function(e) {
	    let verso = document.getElementById('verse');
	    uploadPoem(verso.value.slice(0,140));
	    verso.value = '';
	    e.preventDefault();
	}, false);
}

getPoem();
nuevoVerso();
