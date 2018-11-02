'use strict';
const API = 'http://' + window.location.host + '/api/v1';
const ROOT = 'http://' + window.location.host;
let page = 1;
var book_id = null;

const getBooks = function(page){
  $.ajax({
    method: 'GET',
    url: `${API}/libros/page/${page}`
  }).done(function(res){
    if(res.success){
      addBookDom(res.books);
      if (res.books.length < 24){	document.getElementById('nextPage').classList.add('hiddenButton');
      }
    }else{
      alert('Hubo un problema al cargar los libros');
    }
  });
}

var contador_grupos = 0;
var contador_item = 0;

//Se recorre el objeto JSON
const addBookDom = function(arr){
  arr.forEach(element => {
      //Si el grupo div n que contiene los 3 elementos de tamaño 4 cada uno, se crea un nuevo grupo div n
      if(contador_item == 3){
          contador_item = 0;
          contador_grupos++;
      }
      //Dentro de un grupo div n, se evalua si esta por ingresar el primer elemento o si ya existe
      if(contador_item == 0){
          //Se crea un nuevo grupo div n y dentro de este el primer item (un grupo div n solo puede contener 3 items)
          contador_grupos++;
          $(`#content_books`).append(
              `<div class="row" id="content_group_${contador_grupos}">
                  ${formato_item(element.name, element.author, element.descripcion, element.image, element.file, element.licencia, element.id)}
              </div>`
          );
          contador_item++;

      }else{
          //De existir el primer item en el grupo div n se crean los 2 restantes
          $(`#content_group_${contador_grupos}`).append(
            formato_item(element.name, element.author, element.descripcion, element.image, element.file, element.licencia, element.id)
          );
          contador_item++;
      }
  });
}

//formato_item: devuelve item a item el recorrido del objeto JSON

const titleCase = function(string, tipo){
    if (tipo == 'autor') {
    const strSplit = string.split(' ');
    let strFinal = [];
    let sUp;
    strSplit.forEach(s => {
	sUp = s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
	strFinal.push(sUp);
    });
	return strFinal.join(' ');
    } else if (tipo == 'titulo') {
	return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
    };
}

function formato_item(titulo, autor, descripcion, img, book, licencia, id){
    let tituloBien = titleCase(titulo, 'titulo');
    console.log(tituloBien);
    let autorBien = titleCase(autor, 'autor');
    let licenciaIcon;
    let tituloDom;
    if (licencia == undefined){
	licenciaIcon = "";
    } else if (licencia == "Creative Commons"){
	licenciaIcon = "fab fa-creative-commons"
    } else {
	licenciaIcon = "fab fa-creative-commons-share"
    };
    if (tituloBien.length > 40) {
        tituloDom = `<h3 class="smallTitle">${tituloBien}</h3>`;
    } else{
        tituloDom = `<h3>${tituloBien}</h3>`;
    };
    let contenido_item =
        `<div class="col-md-4 col-sm-4">
            <div class="panel panel-warning">
                <div class="panel-heading">
                    ${tituloDom}
                    <p class="autor">${autorBien}</p>
                </div>
                <div class="panel-body panel-body-background">
                    <div class="col-md-12">
                        <img class="center-block" src="/static/images/${img || 'default.jpg'}" alt="">
                        <a title="Leer libro" href="/static/books/${book}" class="btn btn-primary btn-upload" download><i class="fab fa-readme"></i></a>
                    </div>
                </div>
                <p class="licencia">
                 <a href="#" onclick="openDenounce(${id})" data-toggle="modal" data-target="#denounce" title="Información y Denuncia"><i class="fas fa-info-circle"></i></a>
<a href="/licencias" data-toggle="tooltip" title="${licencia}"><i class="${licenciaIcon}"></i></a>
                </p>
            </div>
        </div>`;

    return contenido_item;
}
// <a href="#" onclick="openDenounce(${id})" data-toggle="modal" data-target="#denounce" title="Información y Denuncia"><i class="fas fa-info-circle"></i></a>

const removeBooksDom = function(){
  const currentBooks = document.getElementById('content_books');
  while (currentBooks.firstChild) {
    currentBooks.removeChild(currentBooks.firstChild);
  }
  contador_grupos = contador_item = 0;
};

const searchInput = function(){
  document.getElementById('filterBooks').addEventListener('submit', function(e) {
      let c = document.getElementById('criteria').value;
      if(c.trim() == '') getBooks(1);
      else filterBooks(c);
      e.preventDefault();
  }, false);
};

let searchPages;
let thisSearchPage;
let searchResults;

const openDenounce = function(id){
  book_id = id;
  console.log(book_id)
}

const denounceBook = function(){
  let desc = document.getElementById('desc').value;
  $.ajax({
    method: 'POST',
    url: `${API}/libro/denounce`,
    data: {desc: desc, id: book_id},
  }).done(function(res){
    alert(res.msg);
  });
}

const filterBooks = function(criteria){
  removeBooksDom();
  $.ajax({
    method: 'GET',
    url: `${API}/libros/search/${criteria}`
  }).done(function(res){
    if(res.success){
      searchResults = res.books;
      thisSearchPage = 1;
      addBookDom(searchResults.slice(0, 24));
      document.getElementById('nextPage').classList.add('hiddenButton');
      searchPages = Math.ceil(searchResults.length/24);
      if (searchPages > 1){
	document.getElementById('nextResults').classList.remove('hiddenButton');
      }
    }else{
      alert('Hubo un problema al cargar los libros');
    }
  });
}

const nextResults = function(){
  document.getElementById('nextResults').addEventListener('click', function(e){
    let nextSearchPage = thisSearchPage + 1
    addBookDom(searchResults.slice(thisSearchPage*24, nextSearchPage*24));
    thisSearchPage = nextSearchPage;
    if (thisSearchPage == searchPages){
      	document.getElementById('nextResults').classList.add('hiddenButton')
    }
  })
};

const nextPage = function(){
  document.getElementById('nextPage').addEventListener('click', function(e) {
    page++;
    getBooks(page);
  })
};

const pageButtons = function(){
  nextResults();
  nextPage();
}

const assignUrlToForm = function(){
  document.getElementById('uploadBook').setAttribute('action', `${API}/libro/upload` )
}

const uploadBook = function(){
  $('#loading').show('slow')
  var form_data = new FormData();
  form_data.append('author', $('#autor').val() );
  form_data.append('book', $('#libro').val() );
  form_data.append('genre', $('#genero').val() );
  form_data.append('language', $('#idioma').val() );
  form_data.append('licence', $('#lice').val() );
  form_data.append('filebook',  $( '#filebook' )[0].files[0]);
  form_data.append('fileimg',  $( '#imagen' )[0].files[0]);
  $.ajax({
      method: 'POST',
      url: `${API}/libro/upload`,
      data: form_data,
      processData: false,
      contentType: false,
  }).done(function(res){
    $('#loading').hide()
    if(!res.success && res.code == 400) alert(res.msg);
    else window.location.href = `${ROOT}/${res.route}`;
  });
}


$('#loading').hide()
getBooks(page);
searchInput();
pageButtons();
// assignUrlToForm();
