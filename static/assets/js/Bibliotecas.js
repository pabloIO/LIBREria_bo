'use strict';
var contador_grupos = 0;
var contador_item = 0;
const BIBLIOS = {
    "BBB": {
        "image": "logoBBB.jpg",
        "books": [
          {
            "id": 1,
            "nombre": "CARTAS PARA COMPRENDER LA HISTORIA DE BOLIVIA",
            "autor": "Mariano Baptista Gumucio",
            "imagen": "CartasParaComprender-750.jpg",
            "archivo": "Cartas para comprender la historia de Bolivia - Mariano Baptista.epub",
            "licencia": "Creative Commons"
          },
          {
            "id": 2,
            "nombre": "SIRINGA. ARREANDO DESDE MOJOS",
            "autor": "Juan B. Coímbra Cuéllar",
            "imagen": "SiringaMojos-750.jpg",
            "archivo": "Siringa. Arreando desde Mojos - Juan B. Coimbra. Rodolfo Pinto Parada.epub",
            "licencia": "Creative Commons"
          },
          {
            "id": 3,
            "nombre": "DIARIO DE UN COMANDANTE DE LA GUERRA DE LA INDEPENDENCIA",
            "autor": "José Santos Vargas",
            "imagen": "tlwp-DiarioComandante_750.png",
            "archivo": "Diario de un comandante de la guerra de la independencia - Jose Santos Vargas.epub",
            "licencia": "Creative Commons"
          },
          {
            "id": 4,
            "nombre": "EL MACIZO BOLIVIANO",
            "autor": "Jaime Mendoza",
            "imagen": "webBBB_0317int001.jpg",
            "archivo": "El Macizo Boliviano - Jaime Mendoza.epub",
            "licencia": "Creative Commons"
          },
          {
            "id": 5,
            "nombre": "JUAN DE LA ROSA",
            "autor": "Nataniel Aguirre",
            "imagen": "bbb-070-JuanDeLaRosa-a.jpg",
            "archivo": "Juan de la Rosa - Nataniel Aguirre.epub",
            "licencia": "Creative Commons"
          },
          {
            "id": 6,
            "nombre": "CUANDO VIBRABA LA ENTRAÑA DE PLATA",
            "autor": "José Enrique Viaña",
            "imagen": "CuandoVibrabaLaEntranaDePlata-750.jpg",
            "archivo": "Cuando Vibraba La Entrana De Plata - Jose Enrique Viana.epub",
            "licencia": "Creative Commons"
          },
          {
            "id": 7,
            "nombre": "ANTOLOGÍA DEL CUENTO BOLIVIANO",
            "autor": "Manuel Vargas Severiche",
            "imagen": "AntologiaCuentoBol-750.jpg",
            "archivo": "Antologia del Cuento Boliviano - Varios autores.epub",
            "licencia": "Creative Commons"
          },
          {
            "id": 8,
            "nombre": "NACIONALISMO Y COLONIAJE",
            "autor": "Carlos Montenegro",
            "imagen": "bbb-160-NacionalismoColoniaje-B.jpg",
            "archivo": "Nacionalismo y Coloniaje - Carlos Montenegro.epub",
            "licencia": "Creative Commons"
          }
        ],
      },
    "FUNDAPPAC": {
        "image": "fundappac.png",
        "books": [
          {
            "id": 1,
            "nombre": "Diccionario Biografico de Parlamentarios 1979 - 2019",
            "autor": "Salvador Romero Ballivian",
            "imagen": "Diccionario Biografico de Parlamentarios.png",
            "archivo": "DiccionarioBiograficoDeParlamentarios1979-2019.pdf",
            "licencia": "libre distribución"
          },
          {
            "id": 2,
            "nombre": "COMPENDIO DE LA LEGISLACIÓN DEL ESTADO PLURINACIONAL DE BOLIVIA",
            "autor": "Israel Ángel Alanoca Chavez",
            "imagen": "pub_20150115_022415_Legislacion Estado Plurinacional de Bolivia.jpg",
            "archivo": "pub_20150115_021301_BALANCE DE LAS  LEYES (ESTADO PLURINACIONAL).pdf",
            "licencia": "libre distribución"
          },
          {
            "id": 3,
            "nombre": "Cuadro Comparativo de Planes de Gobierno. Elecciones Bolivia 2014",
            "autor": "FUNDAPPAC",
            "imagen": "pub_20141013_030307_IMG_20141013_145723307.jpg",
            "archivo": "pub_20141013_030313_Matriz consolidada de programas.xls",
            "licencia": "libre distribución"
          },
          {
            "id": 4,
            "nombre": "NOCHE PARLAMENTARIA: ECONOMÍA Y CAMBIO EN BOLIVIA",
            "autor": "Flavio Machicado, Gonzalo Chávez, Gabriel Loza",
            "imagen": "publicaciones2012a.jpg",
            "archivo": "NOCHE_PARLAMENTARIA_2012_OCT.pdf",
            "licencia": "libre distribución"
          },
          {
            "id": 5,
            "nombre": "PRESUPUESTO PUBLICO PLURINACIONAL PARTICIPATIVO: Una Propuesta de Implamentación Para Bolivia",
            "autor": "Germán Molina Diaz",
            "imagen": "publicaciones2012b.jpg",
            "archivo": "EL_PRESUPUESTO_PUBLICO_2011_AGOSTO.pdf",
            "licencia": "libre distribución"
          },
          {
            "id": 6,
            "nombre": "EL IMPERIO DE TIWANAKU",
            "autor": "publicaciones2010c.jpg",
            "imagen": "publicaciones2011e.jpg",
            "archivo": "EL_IMPERIO_DE_TIWANAKU.PDF",
            "licencia": "libre distribución"
          },
          {
            "id": 7,
            "nombre": "Memorandum Sobre el Mar",
            "autor": "Valentín Abecia Baldivieso, Valentín Abecia López",
            "imagen": "publicaciones2011b.jpg",
            "archivo": "MEMORANDUM_SOBRE_EL_MAR.pdf",
            "licencia": "libre distribución"
          },
          {
            "id": 8,
            "nombre": "Contribución Histórica a los Bicentenarios de Bolivia",
            "autor": "Enrique Rocha Monroy",
            "imagen": "publicaciones2011a.jpg",
            "archivo": "Contribución Histórica a los Bicentenarios de Bolivia.pdf",
            "licencia": "libre distribución"
          },
          {
            "id": 9,
            "nombre": "POA y presupuesto",
            "autor": "Elizabeth Pérez de Garnica, César Calderón Mendoza",
            "imagen": "publicaciones2011c.jpg",
            "archivo": "POA_Y_PRESUPUESTO.pdf",
            "licencia": "libre distribución"
          },
          {
            "id": 10,
            "nombre": "Bolivia: ¿Potencia Energética? Presente y Futuro de los Principales Recursos Energéticos del País",
            "autor": "Francesco Zaratti, Justo P. Zapata Quiroz, Gonzalo H. Rico Calderón, Enrique Velazco Reckling",
            "imagen": "publicaciones2010c.jpg",
            "archivo": "BOLIVIA_POTENCIA_ENERGETICA.PDF",
            "licencia": "libre distribución"
          },
          {
            "id": 11,
            "nombre": "El Presupuesto General del Estado",
            "autor": "Lic. Rubén Ferrufino, Lic. Omar Portada, Lic. Ramiro Quiroga, Lic. Juan Brun, Lic. Germán Molina",
            "imagen": "publicaciones2010b.jpg",
            "archivo": "EL_PRESUPUESTO_GENERAL _DEL_ESTADO.pdf",
            "licencia": "libre distribución"
          },
          {
            "id": 12,
            "nombre": "ABC de los Derechos Humanos de las Mujeres en la Nueva Constitución Política del Estado",
            "autor": "Comisión de Derechos Humanos de la H. Cámara de Diputados",
            "imagen": "publicaciones2009f.jpg",
            "archivo": "ABC DE LOS DERECHOS HUMANOS DE LAS MUJERES.pdf",
            "licencia": "libre distribución"
          },
          {
            "id": 13,
            "nombre": "Autonomía para La Paz",
            "autor": "FUNDAPPAC",
            "imagen": "publicaciones2009e.jpg",
            "archivo": "AUTONOMIA PARA LA PAZ.pdf",
            "licencia": "libre distribución"
          },
          {
            "id": 14,
            "nombre": "Estado y Territorio, La Disputa Post Constitucional",
            "autor": "Gloria Ardaya Salinas",
            "imagen": "publicaciones2009d.jpg",
            "archivo": "ESTADO Y TERRITORIO. LA DISPUTA POST CONSTITUCIONAL.pdf",
            "licencia": "libre distribución"
          },
          {
            "id": 15,
            "nombre": "Hacia Una Nueva Constitución",
            "autor": "José Antonio Rivera S",
            "imagen": "publicaciones2008d.jpg",
            "archivo": "HACIA_UNA_NUEVA_CONSTITUCION.pdf",
            "licencia": "libre distribución"
          },
          {
            "id": 16,
            "nombre": "Manual de los Derechos de los Pueblos Indígenas",
            "autor": "Comisión de Derechos Humanos de la H. Cámara de Diputados",
            "imagen": "publicaciones2009b.jpg",
            "archivo": "MANUAL DE LOS DERECHOS DE LOS PUEBLOS INDIGENAS.pdf",
            "licencia": "libre distribución"
          },
          {
            "id": 17,
            "nombre": "Tristan Marof Supay Pasasan",
            "autor": "Gonzalo Bilbao la Vieja Díaz",
            "imagen": "publicaciones2008b.jpg",
            "archivo": "TRISTAN MAROF - SUPAY PASASAN.pdf",
            "licencia": "libre distribución"
          }
        ]
      },
    "CIS": {
      image: "logo-cis.png",
      books: [
          {
            "id": 1,
            "nombre": "La Nacionalizacion del Sector Electrico en Bolivia",
            "autor": "Hortensia Jiménez Rivera",
            "imagen": "CIS-C-NacionalizacionSectorElectricoBolivia.png",
            "archivo": "La Nacionalizacion del Sector Electrico en Bolivia.pdf",
            "licencia": "CC BY-NC-SA 4.0"
          },
          {
            "id": 2,
            "nombre": "ENCUESTA MUNDIAL DE VALORES EN BOLIVIA 2017",
            "autor": "Sociales y Acción Pública Sociales y Acción Pública Sociales y Acción Pública Sociales y Acción Pública",
            "imagen": "CIS-C-EncuestaMundial2.png",
            "archivo": "Encuesta Mundial de Valores en Bolivia 2017.pdf",
            "licencia": "CC BY-NC-SA 4.0"
          },
          {
            "id": 3,
            "nombre": "EL RESORTE DE LA CONFLICTIVIDAD EN BOLIVIA",
            "autor": "Nicole Jordán Prudencio",
            "imagen": "CIS-C-014.png",
            "archivo": "El resorte de la conflictividad en Bolivia.pdf",
            "licencia": "CC BY-NC-SA 4.0"
          },
          {
            "id": 4,
            "nombre": "INSURGENCIAS FEMENINAS HACIA EL EPICENTRO DEL PODER (SIGLOS XX-XXI) (vol.1)",
            "autor": "Daniela Franco Pinto",
            "imagen": "CIS-C-MujeresBolivianasVol1-tapaFondo.png",
            "archivo": "La Nacionalizacion del Sector Electrico en Bolivia.pdf",
            "licencia": "CC BY-NC-SA 4.0"
          },
          {
            "id": 5,
            "nombre": "PARIDAD Y DIVERSIDAD EN LA ESCENA LEGISLATIVA (vol.2)",
            "autor": "Bianca De Marchi Moyano, Noelia Gómez Téllez",
            "imagen": "CIS-C-MujeresBolivianasVol2-tapaFondo.png",
            "archivo": "Mujeres Bolivianas vol2 - Paridad y diversidad en la escena legislativa.pdf",
            "licencia": "CC BY-NC-SA 4.0"
          },
          {
            "id": 6,
            "nombre": "POLÍTICA Y ROMANCE EN LA CANDIDATURA DE ROJAS, DE ARMANDO CHIRVECHES",
            "autor": "Pedro E. Brusiloff Díaz-Romero",
            "imagen": "cis-PoliticaRomanceCandidatura-B.jpg",
            "archivo": "Politica y Romance en la Candidatura de Rojas, de Armando Chirveches - Brusiloff, Pedro E..pdf",
            "licencia": "CC BY-NC-SA 4.0"
          },
          {
            "id": 7,
            "nombre": "CHICHERAS DE LA CIUDAD DE ORURO",
            "autor": "Luisa Andrea Cazas Aruquipa",
            "imagen": "cis-ChicherasCiudadOruro-a.jpg",
            "archivo": "Chicheras de la Ciudad de Oruro - Luisa Andrea Cazas Aruquipa.pdf",
            "licencia": "CC BY-NC-SA 4.0"
          },
          {
            "id": 8,
            "nombre": "BOLIVIA: ESCENARIOS EN TRANSFORMACIÓN. ARTÍCULOS SOBRE POLÍTICA, CULTURA Y ECONOMÍA",
            "autor": "Varios",
            "imagen": "cis-a-BoliviaEscenariosTransformacion.jpg",
            "archivo": "Bolivia Escenarios en Transformacion.pdf",
            "licencia": "CC BY-NC-SA 4.0"
          },
          {
            "id": 9,
            "nombre": "BOLIVIA DIGITAL",
            "autor": "Varios",
            "imagen": "BBB-C-BoliviaDigital-01.png",
            "archivo": "Bolivia Digital. 15 Miradas acerca del Internet y Sociedad en Bolivia - Varios autores.pdf",
            "licencia": "CC BY-NC-SA 4.0"
          },
          {
            "id": 10,
            "nombre": "QUÉ ES LA GEOGRAFÍA",
            "autor": "Ruy Moreira",
            "imagen": "CIS-C-QueEsLaGeografia.png",
            "archivo": "Ruy Moreira, Que es la Geografia - CIS.pdf",
            "licencia": "CC BY-NC-SA 4.0"
          }
        ]
    }
};


const chooseLibrary = function(name){
  console.log(name);
  addBookLibrary(name, 'content_library');
}

const addBookLibrary = function(key, id){
  var lib = BIBLIOS[key];
  var c = document.getElementById(id);
  c.parentNode.removeChild(c);
  let div = document.createElement('div');
  div.setAttribute('id', 'content_library')
  document.getElementById('container_library').appendChild(div)
  document.getElementById('img-library').setAttribute('src', `static/assets/img/${lib.image}`);
  lib.books.forEach(element => {
      //Si el grupo div n que contiene los 3 elementos de tamaño 4 cada uno, se crea un nuevo grupo div n
      if(contador_item == 3){
          contador_item = 0;
          contador_grupos++;
      }
      //Dentro de un grupo div n, se evalua si esta por ingresar el primer elemento o si ya existe
      if(contador_item == 0){
          //Se crea un nuevo grupo div n y dentro de este el primer item (un grupo div n solo puede contener 3 items)
          contador_grupos++;
          $(`#${id}`).append(
              `<div class="row" id="content_group_${contador_grupos}">
                  ${formato_item_biblio(element.nombre, element.autor, element.descripcion, element.imagen, element.archivo, element.licencia)}
              </div>`
          );
          contador_item++;

      }else{
          //De existir el primer item en el grupo div n se crean los 2 restantes
          $(`#content_group_${contador_grupos}`).append(
            formato_item_biblio(element.nombre, element.autor, element.descripcion, element.imagen, element.archivo, element.licencia)
          );
          contador_item++;
      }
  });
}

function formato_item_biblio(titulo, autor, descripcion, img, book, licencia){
    let licenciaIcon;
    if (licencia == undefined){
	licenciaIcon = "";
    } else if (licencia == "Creative Commons"){
	licenciaIcon = '<p class="licencia"><a href="/licencias" data-toggle="tooltip" title="Creative Commons"><i class="fab fa-creative-commons"></i></a></p>'
    } else {
	licenciaIcon = '<p class="licencia"><a href="/licencias" data-toggle="tooltip" title="Dominio público"><i class="fab fa-creative-commons-share"></i></a></p>'
    };
    let contenido_item =
        `<div class="col-md-4 col-sm-4">
            <div class="panel panel-warning">
                <div class="panel-heading">
                    <h3>${titulo}</h3>
                    <p class="autor">${autor}</p>
                </div>
                <div class="panel-body panel-body-background">
                    <div class="col-md-12">
                        <img class="center-block" src="/static/libraries/images/${img || 'default.jpg'}" alt="" style="width:auto;height:300px">
                        <a title="Leer libro" href="/static/libraries/books/${book}" class="btn btn-primary btn-upload" download><i class="fab fa-readme"></i></a>
                    </div>
                </div>
                ${licenciaIcon}
            </div>
        </div>`;

    return contenido_item;
}

addBookLibrary("BBB", 'content_library');
