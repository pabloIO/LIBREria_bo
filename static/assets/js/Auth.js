'use strict';
var Auth = (function(){
    /**
     * @keys: [id, username, token, socket_channel, _conversation_id, sesion]
     */
    let conversation = [];
    let _storage = LocalStorage;
    function login(){
        let creds = {
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        };
        if(creds.username == '' || creds.password == '' ) {
            alert('Debe llenar ambos campos');
            return;
        }
        $.ajax({
            method: 'POST',
            url : `${Config.PUBLIC_URL}/login`,
            headers: {
                'Content-Type': 'application/json'
            },
            data: JSON.stringify(creds),
            success: function(response){
                console.log(response)
                if(response.success && response.code == 200){
                    // conversation = response.conversation;
                    // conv = response.conversation;
                    LocalStorage.setKeys(response.user)
                    console.log('hey')
                    window.location.href = `${Config.URL}/user/dashboard`
                }else{
                    alert(response.msg);
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    }
    function signIn(){
        // if (document.getElementById("password").value !== ){

        // }
        let creds = {
            username: document.getElementById("username").value,
            name: document.getElementById("name").value,
            lastname: document.getElementById("lastname").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value,
        };
        $.ajax({
            method: 'POST',
            url : `${Config.PUBLIC_URL}/sign_in`,
            headers: {
                'Content-Type': 'application/json'
            },
            data: JSON.stringify(creds),
            success: function(response){
                console.log(response)
                if(response.success && response.code == 200){
                    // conversation = response.conversation;
                    // conv = response.conversation;
                    window.location.href = `${Config.URL}/`
                }else{
                    alert(response.msg);
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    }
    function logout(){
        LocalStorage.unsetKeys();
        $.ajax({
            method: 'POST',
            url : `${Config.PUBLIC_URL}/user/logout`,
            headers: {
                'Content-Type': 'application/json'
            },
            data: JSON.stringify({success: true}),
            success: function(response){
                console.log(response)
                if(response.logout){
                    // conversation = response.conversation;
                    // conv = response.conversation;
                    window.location.href = `${Config.URL}`
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
                if(response){
                    // conversation = response.conversation;
                    conv = response.conversation;
                }else{
                    alert(response.msg);
                }
            }
        });
    }

    return{
        getConversation: getConversation,
        login: login,
        logout: logout,
        signIn: signIn
    };
})();
