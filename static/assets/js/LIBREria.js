'use strict';
// var LIBREria = (function(){

// }());

let page = 1;
var book_id = null;
document.getElementById('autor').setAttribute('value', LocalStorage.getKey('name'));

const getBooks = function(page){
  $.ajax({
    method: 'GET',
    url: `${Config.PUBLIC_URL}/libros/page/${page}`,
    headers: {
      'Authorization': `Bearer ${LocalStorage.getKey('token')}`
    },
  }).done(function(res){
    if(res.success){
      console.log(res);
      addBookDom(res.books);
      if (res.books.length < 24) document.getElementById('nextPage').classList.add('hiddenButton');
    }else{
      alert('Hubo un problema al cargar los libros');
    }
  });
}


function getBook(){
  var id = window.location.pathname.split('/').reverse()[0];
  // console.log(id)
  // console.log(id)
  $.ajax({
    method: 'GET',
    url: `${Config.PUBLIC_URL}/libros/${id}`,
    headers: {
      'Authorization': `Bearer ${LocalStorage.getKey('token')}`
    },
  }).done(function(res){
    console.log(res)
    if(res.success){
      document.getElementById('img_book').setAttribute('src', `${Config.URL}/static/images/${res.book.image || 'default.png'}`);
      document.getElementById('download_button').setAttribute('href', `${Config.URL}/static/books/${res.book.file}`);
      document.getElementById("download_button").addEventListener("click", downloadBook);
      document.getElementById("title").innerHTML = res.book.title;
      // /static/books/${book}
      $('#num_downloads').text(`${res.book.downloads}`);
      res.book.comments.map((e, i) => {
        $('#comments').append(
            `<li class="clearfix">
                <span class="chat-img pull-left">
                    <img src="" class="img-circle" /> 
                </span> 
                <div class="chat-body clearfix"> 
                    <div class="header"> 
                        <a class="primary-font" href="/user/perfil/${e.autor_id}" ><i>@${e.autor}</i></a> 
                        <small class="pull-right text-muted"> 
                            <span class="glyphicon glyphicon-time"></span>
                              ${e.date}
                        </small>
                    </div>
                    <p> ${e.text} </p> 
                </div> 
                </li>`
        );
      });
      
      $('#word_cloud').jQCloud(res.book.keywords, {
        width: 450, 
        height: 350, 
        fontSize: {
          from: 0.05,
          to: 0.04
        }
      });
    }else{
      alert(res.msg);
    }
  });
}

function downloadBook(){
  var id = window.location.pathname.split('/').reverse()[0];
  $.ajax({
    method: 'GET',
    url: `${Config.PUBLIC_URL}/libro/download/${id}`,
    headers: {
      'Authorization': `Bearer ${LocalStorage.getKey('token')}`
    },
  }).done(function(res){
    if(res.success){
        $('#num_downloads').text(`Descargas: ${res.downloads_counter}`);
    }else{
      console.warn(res);
    }
  });
}

var contador_grupos = 0;
var contador_item = 0;

//Se recorre el objeto JSON
const addBookDom = function(arr, show_info){
  console.log(arr, show_info)
  arr.map(element => {
      console.log(show_info);
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
                  ${formato_item(element, show_info)}
              </div>`
          );
          contador_item++;

      }else{
          //De existir el primer item en el grupo div n se crean los 2 restantes
          $(`#content_group_${contador_grupos}`).append(
            formato_item(element, show_info)
          );
          contador_item++;
      }
  });
}

//formato_item: devuelve item a item el recorrido del objeto JSON

const titleCase = function(string, tipo){
    console.log(string)
    if (tipo == 'autor') {
      const strSplit = string.split(' ');
      let strFinal = [];
      let sUp;
      strSplit.forEach(s => {
        sUp = s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
        strFinal.push(sUp);
      });
      return strFinal.join(' ');
    }else if (tipo == 'titulo') {
     return `${string.charAt(0).toUpperCase()}${string.slice(1).toLowerCase()}`;
    }
}
// titulo, autor, descripcion, img, book, licencia, id, show_info
function formato_item(book, show_info){
    let tituloBien = titleCase(book.name, 'titulo');
    let licenciaIcon;
    let tituloDom;
    if (book.licencia == undefined){
    licenciaIcon = "";
      } else if (book.licencia == "Creative Commons"){
    licenciaIcon = "fab fa-creative-commons"
      } else {
    licenciaIcon = "fab fa-creative-commons-share"
      };
    if (tituloBien.length > 40) {
        tituloDom = `<h3 class="smallTitle">${tituloBien}</h3>`;
    } else{
        tituloDom = `<h3>${tituloBien}</h3>`;
    };
    let contenido_item;
    if(!show_info){
      contenido_item =
      `<div class="col-md-4 col-sm-4">
          <div class="panel panel-warning">
              <div class="panel-heading">
                <a href="/user/libro/${book.id}">${tituloDom}</a>
                <a class="text-center" href="${Config.URL}/user/perfil/${book.autor.autor_id}">
                  <i>@${book.autor.name}</i>
                </a>
              </div>
              <div class="panel-body panel-body-background">
                  <div class="col-md-12">
                      <img class="center-block" src="/static/images/${book.image || 'default.png'}" alt="">
                      <a title="Leer libro" href="/static/books/${book.file}" class="btn btn-primary btn-upload" download><i class="fab fa-readme"></i></a>
                  </div>
              </div>
              <p class="licencia">
               <a href="#" onclick="openDenounce(${book.id})" data-toggle="modal" data-target="#denounce" title="Información y Denuncia"><i class="fas fa-info-circle"></i></a>
               <a href="/licencias" data-toggle="tooltip" title="${book.licencia}"><i class="${book.licenciaIcon}"></i></a>
              </p>
          </div>
      </div>`;
    }else{
      contenido_item =
      `<div class="col-md-4 col-sm-12">
          <div class="panel panel-warning">
              <div class="panel-heading">
                  <a href="/user/libro/${book.id}">${tituloDom}</a>
              </div>
              <div class="panel-body panel-body-background">
                  <div class="col-md-12">
                      <img class="center-block" src="/static/images/${book.image || 'default.png'}" alt="">
                      <a title="Ver estadísticas" href="${Config.URL}/user/autor/my-books/${book.id}" class="btn btn-primary btn-upload"><i class="fas fa-chart-bar"></i></a>
                  </div>
              </div>
              <p class="licencia">
               <a href="#" onclick="openDenounce(${book.id})" data-toggle="modal" data-target="#denounce" title="Información y Denuncia"><i class="fas fa-info-circle"></i></a>
<a href="/licencias" data-toggle="tooltip" title="${book.licencia}"><i class="${licenciaIcon}"></i></a>
              </p>
          </div>
      </div>`;
    }
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
    url: `${Config.PUBLIC_URL}/libro/denounce`,
    data: {desc: desc, id: book_id},
    headers: {
      'Authorization': `Bearer ${LocalStorage.getKey('token')}`
    },
  }).done(function(res){
    alert(res.msg);
  });
}

const filterBooks = function(criteria){
  removeBooksDom();
  $.ajax({
    method: 'GET',
    url: `${Config.PUBLIC_URL}/libros/search/${criteria}`,
    headers: {
      'Authorization': `Bearer ${LocalStorage.getKey('token')}`
    },
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
  form_data.append('autor_id', LocalStorage.getKey('autor_id'));

  $.ajax({
      method: 'POST',
      url: `${Config.PUBLIC_URL}/libro/upload`,
      data: form_data,
      headers: {
        'Authorization': `Bearer ${LocalStorage.getKey('token')}`
      },
      processData: false,
      contentType: false,
  }).done(function(res){
    $('#loading').hide()
    if(!res.success && res.code == 400) alert(res.msg);
    else window.location.href = `${Config.URL}/${res.route}/${res.book_id}`;
  });
}
