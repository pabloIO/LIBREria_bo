'use strict';
var User = (function(){
    /**
     * @keys: [id, username, token, socket_channel, _conversation_id, sesion]
     */
    // let conversation = [];
    let _storage = LocalStorage;
    function getUserData(){
        var id = _storage.getKey('id');
        $.ajax({
            method: 'GET',
            url : `${Config.PUBLIC_URL}/profile/${id}`,
            headers: {
                'Content-Type': 'application/json'
            },
            success: function(res){
                if(res.success){
                    $('#name').text(res.user.name);
                    $('#username').text(`@${res.user.username}`);
                    document.getElementById('user_img').setAttribute('src', `${Config.URL}/static/users/${res.user.image || 'default_user.png'}`)
                }else{
                    alert(response.msg);
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    }
    function getUser(id){
        $.ajax({
            method: 'GET',
            url : `${Config.PUBLIC_URL}/profile/${id}`,
            headers: {
                'Content-Type': 'application/json'
            },
            success: function(res){
                if(res.success){
                    $('#name').text(res.user.name);
                    $('#username').text(`@${res.user.username}`);
                    document.getElementById('user_img').setAttribute('src', `${Config.URL}/static/users/${res.user.image || 'default_user.png'}`)
                }else{
                    alert(response.msg);
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    }
    function getAuthor(){
        var path = window.location.pathname.split('/').reverse();
        var id = !Number.isInteger(Number(path[0])) || path[1] == 'my-books' 
                ? LocalStorage.getKey('autor_id') : window.location.pathname.split('/').reverse()[0];
        var isMine = !Number.isInteger(Number(path[0])) || path[1] == 'my-books';
        if(!isMine){
            $('#autor_books').hide();
            $('#config').hide();
            $('#stats-books').hide()
        }
        
        $.ajax({
            method: 'GET',
            url : `${Config.PUBLIC_URL}/profile-author/${id}`,
            headers: {
                'Content-Type': 'application/json'
            },
            success: function(res){
                if(res.success){
                    $('#name').text(res.user.name);
                    $('#username').text(`@${res.user.username}`);
                    document.getElementById('user_img').setAttribute('src', `${Config.URL}/static/users/${res.user.image || 'default_user.png'}`)
                }else{
                    alert(response.msg);
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    }
    function getFollowers(){
        var id = _storage.getKey('autor_id');
        $.ajax({
            method: 'GET',
            url : `${Config.PUBLIC_URL}/followers/${id}`,
            headers: {
                'Content-Type': 'application/json'
            },
            success: function(res){
                if(res.success){
                    if(res.followers.length == 0){
                        $('#followers').append('<h4 class="text-center">No tienes seguidores</h4>')
                    }else{
                        res.followers.map((e, i) => {
                            var bio = e.bio 
                                ? e.bio.length > 100 
                                    ? e.bio.slice(0, 100) + ' ...' : e.bio 
                                : '';
                            $('#followers').append(
                                `<div class="col-sm-12 col-md-6">
                                        <div class="cuadro-user">
                                            <div class="caja-user">
                                                <div class="image-user">
                                                    <a  href="${Config.URL}/user/perfil/${e.autor_id}">
                                                        <img src="/static/users/${e.image || 'default_user.png'}">
                                                    </a>
                                                </div>
                                                <h4> ${e.name} <br>
                                                    <span> @${e.username} </span>
                                                </h4>
                                                <p>${bio}</p>
                                                <a class="btn btn-seguir">Seguir</a>   
                                            </div>
                                        </div>
                                    </div>`
                            )
                        });
                    }
                }else{
                    alert(response.msg);
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    }
    function getFollowing(){
        var id = _storage.getKey('autor_id');
        $.ajax({
            method: 'GET',
            url : `${Config.PUBLIC_URL}/following/${id}`,
            headers: {
                'Content-Type': 'application/json'
            },
            success: function(res){
                if(res.success){
                    if(res.following.length == 0){
                        $('#following').append('<h4 class="text-center">No sigues a nadie, busca a otros autores</h4>')
                    }else{
                        res.following.map((e, i) => {
                            var bio = e.bio 
                                ? e.bio.length > 100 
                                    ? e.bio.slice(0, 100) + ' ...' : e.bio 
                                : ''; 
                            $('#following').append(
                                `<div class="col-sm-12 col-md-6">
                                        <div class="cuadro-user">
                                            <div class="caja-user">
                                                <div class="image-user">
                                                    <a  href="${Config.URL}/user/perfil/${e.autor_id}">
                                                        <img src="/static/users/${e.image || 'default_user.png'}">
                                                    </a>
                                                </div>
                                                <h4> ${e.name} <br>
                                                    <span> @${e.username} </span>
                                                </h4>
                                                <p> ${bio} </p>
                                                <a class="btn btn-no-seguir">Siguiendo</a>   
                                            </div>
                                        </div>
                                    </div>`
                            )
                        });
                    }
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
    function isFollowing(){
        var path = window.location.pathname.split('/').reverse();
        var followed_id = Number.isInteger(Number(path[0])) 
                ?  window.location.pathname.split('/').reverse()[0] : null;
        var id = LocalStorage.getKey('autor_id');
        // console.log(followed_id)
        if(id == followed_id || path[0] == 'perfil' || path[0] == 'followers' || path[0] == 'following') return;
        $.ajax({
            method: 'GET',
            url : `${Config.PUBLIC_URL}/following/${id}/${followed_id}`,
            headers: {
                'Content-Type': 'application/json'
            },
            success: function(res){
                if(res.success){
                    console.log(res);
                    var btn = document.createElement('button');
                    btn.id = 'follow-btn';
                    btn.addEventListener('click', function(){ followUser(res.following, id, followed_id) });
                    if(res.following){
                        btn.className = 'btn btn-primary';
                        var t = document.createTextNode('Dejar de seguir');
                        btn.appendChild(t);
                    }else{
                        btn.className = 'btn btn-default';
                        var t = document.createTextNode('Seguir');
                        btn.appendChild(t);
                    }
                    document.getElementById('following-container').appendChild(btn);
                }else{
                    alert(response.msg);
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    }
    function followUser(isFollowing, mId, followedId){
        var data = {
            isFollowing: Boolean(isFollowing),
            user_id: mId, 
            followed_id: followedId
        };
        $.ajax({
            method: 'POST',
            url : `${Config.PUBLIC_URL}/follow`,
            headers: {
                'Content-Type': 'application/json'
            },
            data: JSON.stringify(data),
            success: function(response){
                if(response.success){
                    document.getElementById('follow-btn').className = response.follow ? 'btn btn-primary' : 'btn btn-default';
                    document.getElementById('follow-btn').innerHTML = response.follow ? 'Dejar de seguir' : 'Seguir';
                    document.getElementById('follow-btn').addEventListener('click', function(){ followUser(response.follow, data.user_id, data.followed_id) });
                }else{
                    alert(response.msg);
                }
            }
        });
    }

    function getBooksStats(){
        $.ajax({
            method: 'GET',
            url: `${Config.PUBLIC_URL}/profile/books/stats/${LocalStorage.getKey('autor_id')}`,
            headers: {
              'Authorization': `Bearer ${LocalStorage.getKey('token')}`,
              'Content-Type': 'application/json'
            },
          }).done(function(res){
              console.log(res);
              if(res.success){
                $('#name_autor').text(LocalStorage.getKey('name'));
                var ctxC = document.getElementById('line_chart').getContext('2d');
                $('#keyword_word_cloud').jQCloud(res.word_cloud_keywords, {
                    autoResize: true,
                    width: 700,
                    height: 400
                });
                var comparisonChart = new Chart(ctxC, {
                    type: 'line',
                    data: {
                        labels: res.books.map((e,i) => e.title),
                        datasets: [{
                            label: 'Descargas',
                            data: res.books.map((e,i) => e.downloads),
                            backgroundColor: [
                                'rgba(255,255,255, 0.2)',
                            ],
                            borderColor: [
                                'rgb(190,224,221)',
                            ],
                            borderWidth: 2,
                            borderRadius: 3,
                            pointHoverBackgroundColor: '#fbf7c8',
                            pointHoverBorderColor: 'fbf7c8',
                            pointHoverRadius: 6
                        },{
                            label: 'Vistas',
                            data: res.books.map((e,i) => e.views),
                            backgroundColor: [
                                'rgba(255,255,255, 0.2)',
                            ],
                            borderColor: [
                                'rgb(253,185,163)',
                            ],
                            borderWidth:2,
                            borderRadius: 3,
                            pointHoverBackgroundColor: '#fbf7c8',
                            pointHoverBorderColor: 'fbf7c8',
                            pointHoverRadius: 6
                        },{
                            label: 'Rating',
                            data: res.books.map((e,i) => e.likes),
                            backgroundColor: [
                                'rgba(255,255,255, 0.2)',
                            ],
                            borderColor: [
                                'rgb(132,42,191)',
                            ],
                            borderWidth: 2,
                            borderRadius: 3,
                            pointHoverBackgroundColor: '#fbf7c8',
                            pointHoverBorderColor: 'fbf7c8',
                            pointHoverRadius: 6
                        }]
                    },
                    options: {
                        scales: {
                            yAxes: [{
                                ticks: {
                                    beginAtZero:false
                                }
                            }],
                            xAxes: [{
                                ticks: {
                                    fontSize: 10
                                }
                            }]
                        }
                    }
                });
              }else{
                  alert(res.msg)
              }
        });
    }

    return{
        getUserData: getUserData,
        getBooks: getBooks,
        getUser: getUser,
        isFollowing: isFollowing,
        getAuthor: getAuthor,
        getFollowers: getFollowers,
        getFollowing: getFollowing,
        getBooksStats: getBooksStats,
    };
})();
