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
    function getAuthor(id){
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
                console.log(res)
                if(res.success){
                    if(res.followers.length == 0){
                        $('#followers').append('<h4 class="text-center">No tienes seguidores</h4>')
                    }else{
                        res.followers.map((e, i) => {
                            $('#followers').append(
                                `<a  href="${Config.URL}/user/perfil/${e.autor_id}">    
                                    <div class="col-sm-12 col-md-4">
                                        <img class="center-block" src="/static/users/${e.image || 'default_user.png'}" alt="">
                                        <h3> ${e.name} </h3>
                                        <h4><i> @${e.username} </i></h4>
                                    </div>
                                </a>`
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
                console.log(res)
                if(res.success){
                    if(res.following.length == 0){
                        $('#following').append('<h4 class="text-center">No sigues a nadie, busca a otros autores</h4>')
                    }else{
                        res.following.map((e, i) => {
                            $('#following').append(
                                `<a  href="${Config.URL}/user/perfil/${e.autor_id}">    
                                    <div class="col-sm-12 col-md-4">
                                        <img class="center-block" src="/static/users/${e.image || 'default_user.png'}" alt="">
                                        <h3> ${e.name} </h3>
                                        <h4><i> @${e.username} </i></h4>
                                    </div>
                                </a>`
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
    function isFollowing(followed_id){
        var id = _storage.getKey('autor_id');
        console.log(followed_id)
        if(id == followed_id || followed_id == 'perfil') return;
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

    return{
        getUserData: getUserData,
        getBooks: getBooks,
        getUser: getUser,
        isFollowing: isFollowing,
        getAuthor: getAuthor,
        getFollowers: getFollowers,
        getFollowing: getFollowing,
    };
})();
