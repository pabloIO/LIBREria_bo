'use strict';
const API = 'http://' + window.location.host + '/api/v1';
let poema = [];
const poem = document.getElementById('poemafinal');

const getPoem = function (){
    $.ajax({
	method: 'GET',
	url: `${API}/poems/page`
    }).done(function(res){
	if(res.success){
	    res.books.forEach(v => {
		poema.push(v.verso);
	    });
            displayPoem(poema);
	}else{
	    alert('Hubo un problema en la recuperación de datos');
	}
    });
}

let versos = []
const displayPoem = function(poema, status){
    poema.forEach(v => {
	let verso = document.createElement('p');
	verso.textContent = v;
	verso.classList.add('finalVerso', 'oculto');
	poem.appendChild(verso);
	versos.push(verso);
	let separator = document.createElement('p');
	separator.textContent = " · "
	separator.classList.add('separator')
	poem.appendChild(separator);
    });
    versoVisto(versos);
}

const versoVisto = function(versos) {
    $(document).on("scroll", function () {
	let pageTop = $(document).scrollTop()
	let pageBottom = pageTop + $(window).height()

	for (let i = 0; i < versos.length; i++) {
	    let verso = versos[i]

	    if ($(verso).position().top < pageBottom) {
		console.log(i)
		$(verso).addClass("visible")
	    } else {
		$(verso).removeClass("visible")
	    }
	}
    })
}

getPoem();


