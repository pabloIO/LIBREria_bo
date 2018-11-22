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
                console.log(res)
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
    function getConversation(id){
        // alert(request);
        let user_id = id;
        var conv = null;
        $.ajax({
            method: 'GET',
            url : `http://192.168.0.107:3000/user/${user_id}/conversation`,
            async: false,
            success: function(response){
                if(response.success){
                    // conversation = response.conversation;
                    conv = response.conversation;
                }else{
                    alert(response.msg);
                }
            }
        });
    }

    return{
        getUserData: getUserData,
        getBooks: getBooks,
    };
})();
