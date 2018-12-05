'use strict';
var Book = (function(){
    /**
     * @keys: [id, username, token, socket_channel, _conversation_id, sesion]
     */
    let _storage = LocalStorage;
    var book_id = window.location.pathname.split('/').reverse()[0];
    function getBookStats(){
        // var book_id = window.location.pathname.split('/').reverse()[0];
        $.ajax({
            method: 'GET',
            url : `${Config.PUBLIC_URL}/profile/books/info/${book_id}`,
            headers: {
                'Content-Type': 'application/json'
            },
            success: function(res){
                console.log(res)
                if(res.success){
                    $('#word_cloud_book').jQCloud(res.book.keywords, {
                        width: 450, 
                        height: 350, 
                    });
                    $('#comment_word_cloud').jQCloud(res.comment_wc, {
                        width: 450, 
                        height: 350, 
                    });
                    $('#book_title').text(res.book.title);
                    var ctx = document.getElementById('word_cloud_book_chart').getContext('2d');
                    var labels = res.book.keywords.map((e, i ) => e.text).slice(0,30);
                    var key_word_count = res.book.keywords.map((e, i ) => e.weight).slice(0,30);
                    var myBarChart = new Chart(ctx, {
                        type: 'horizontalBar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: '30 palabras más importantes',
                                data: key_word_count,
                                backgroundColor: [
                                    'rgba(255, 99, 132, 0.2)',
                                    'rgba(54, 162, 235, 0.2)',
                                    'rgba(255, 206, 86, 0.2)',
                                    'rgba(75, 192, 192, 0.2)',
                                    'rgba(153, 102, 255, 0.2)',
                                    'rgba(255, 159, 64, 0.2)'
                                ],
                                borderColor: [
                                    'rgba(255,99,132,1)',
                                    'rgba(54, 162, 235, 1)',
                                    'rgba(255, 206, 86, 1)',
                                    'rgba(75, 192, 192, 1)',
                                    'rgba(153, 102, 255, 1)',
                                    'rgba(255, 159, 64, 1)'
                                ],
                                borderWidth: 1
                            }]
                        },
                        options: {
                            scales: {
                                yAxes: [{
                                    ticks: {
                                        beginAtZero:true
                                    }
                                }]
                            }
                        }
                    });
                    var ctxC = document.getElementById('comparison_chart').getContext('2d');
                    var comparisonChart = new Chart(ctxC, {
                        type: 'bar',
                        data: {
                            labels: ['# descargas', '# visitas'],
                            datasets: [{
                                label: 'visitas vs. descargas',
                                data: [res.book.downloads, res.book.views,],
                                backgroundColor: [
                                    'rgba(255, 99, 132, 0.2)',
                                    'rgba(54, 162, 235, 0.2)',
                                    'rgba(255, 206, 86, 0.2)',
                                    'rgba(75, 192, 192, 0.2)',
                                    'rgba(153, 102, 255, 0.2)',
                                    'rgba(255, 159, 64, 0.2)'
                                ],
                                borderColor: [
                                    'rgba(255,99,132,1)',
                                    'rgba(54, 162, 235, 1)',
                                    'rgba(255, 206, 86, 1)',
                                    'rgba(75, 192, 192, 1)',
                                    'rgba(153, 102, 255, 1)',
                                    'rgba(255, 159, 64, 1)'
                                ],
                                borderWidth: 1
                            }]
                        },
                        options: {
                            scales: {
                                yAxes: [{
                                    ticks: {
                                        beginAtZero:true
                                    }
                                }]
                            }
                        }
                    });
                }else{
                    alert(response.msg);
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    }
    function getBooks(show_info_btn){
        var id = _storage.getKey('autor_id');
        $.ajax({
            method: 'GET',
            url : `${Config.PUBLIC_URL}/profile/books/${id}`,
            headers: {
                'Content-Type': 'application/json'
            },
            success: function(res){
                console.log(res)
                if(res.success){
                    addBookDom(res.book.books, show_info_btn);
                    if (res.book.books.length < 24) document.getElementById('nextPage').classList.add('hiddenButton');
                }else{
                    alert(response.msg);
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    }
    function denounceBook(){
        let desc = document.getElementById('desc').value.split();
        if(desc == ''){
            alert('Debe escribir su denuncia');
            return;
        }
        var book_id = window.location.pathname.split('/').reverse()[0];
        var data = {
            desc: desc,
            autor_id: LocalStorage.getKey('autor_id')
        }; 
        $.ajax({
          method: 'PUT',
          url: `${Config.PUBLIC_URL}/libro/${book_id}/denounce`,
          data: JSON.stringify(data),
          headers: {
            'Authorization': `Bearer ${LocalStorage.getKey('token')}`,
            'Content-Type': 'application/json'
          },
        }).done(function(res){
            if(res.success){
                alert(res.msg)
                setTimeout(() => {
                    $('#desc').text('');
                    $('#denounce').modal('hide');
                }, 2000);
            }else{
                alert(res);
            }
        });
    }

    function renderStars(){
        var container = $('#stars');
        var points = [1,2,3,4,5];
        points.map((e, i) => {
            console.log(e);
            var input = document.createElement('input');
            input.id = `star${e}`
            input.setAttribute('type', 'radio');
            input.setAttribute('name', 'estrellas');
            input.addEventListener('click', function(){ rateBook(e)});

            container.prepend(
                input,
                `<label class="starrr" for="star${e}">★</label>`
            );
        })
    }

    function rateBook(rating){
        // var book_id = window.location.pathname.split('/').reverse()[0];
        var data = {
            rating: rating,
            autor_id: LocalStorage.getKey('autor_id')
        }; 
        console.log(data);
        console.log(rating)
        // return;
        $.ajax({
            method: 'PUT',
            url: `${Config.PUBLIC_URL}/libro/${book_id}/rate`,
            data: JSON.stringify(data),
            headers: {
              'Authorization': `Bearer ${LocalStorage.getKey('token')}`,
              'Content-Type': 'application/json'
            },
          }).done(function(res){
              if(res.success){
                for (let index = 0; index < rating; index++) {
                    document.getElementById(`star${index+1}`)
                            .setAttribute('checked', true);
                }
              }
        });
    }

    function getRating(){
        var autor_id = LocalStorage.getKey('autor_id');
        $.ajax({
            method: 'GET',
            url: `${Config.PUBLIC_URL}/libro/${book_id}/rate/${autor_id}`,
            headers: {
              'Authorization': `Bearer ${LocalStorage.getKey('token')}`,
              'Content-Type': 'application/json'
            },
          }).done(function(res){
              console.log(res);
              if(res.success){
                for (let index = 0; index < res.rating; index++) {
                    document.getElementById(`star${index+1}`)
                            .setAttribute('checked', true);
                }
              }
        });
    }

    return{
        getBookStats: getBookStats,
        denounceBook: denounceBook,
        renderStars: renderStars,
        rateBook: rateBook,
        getRating: getRating,
    };
})();
