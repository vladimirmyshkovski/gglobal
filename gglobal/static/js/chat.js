window.onload = function() {

function runScript(e) {
    if (e.keyCode == 13) {
        var tb = document.getElementById("scriptBox");
        eval(tb.value);
        return false;
    }
}

var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
// Note that the path doesn't matter for routing; any WebSocket
// connection gets bumped over to WebSocket consumers
websocket = new WebSocket(ws_scheme + "://" + window.location.host + "/chat/");
//socket.onmessage = function(e) {
//    //alert(e.data);
//}
websocket.onopen = function() {
    websocket.send("connect");
}

websocket.onmessage = function(e) {
var data =  jQuery.parseJSON(e.data);

if (data.sender = 'user') {
    message =   '<div class="row msg_container base_receive">' +
                    '<div class="col-md-2 col-xs-2 avatar">' +
                        '<img src="http://www.bitrebels.com/wp-content/uploads/2011/02/Original-Facebook-Geek-Profile-Avatar-1.jpg" class=" img-responsive ">' +
                    '</div>' +

                    '<div class="col-xs-10 col-md-10">' +
                        '<div class="messages msg_receive">' +
                            '<p>' + data.message + '</p>' + '<time datetime="">' + data.time + '</time>' + 
                        '</div>' +
                    '</div>' +
                '</div>';

    $('.msg_container_base').append(message);
} else {
    message =   '<div class="row msg_container base_send">' +
                    '<div class="col-xs-10 col-md-10">' +
                        '<div class="messages msg_send">' +
                            '<p>' + data.message + '</p>' + '<time datetime="">' + data.time + '</time>' + 
                        '</div>' +
                    '</div>' +

                    '<div class="col-md-2 col-xs-2 avatar">' +
                        '<img src="http://www.bitrebels.com/wp-content/uploads/2011/02/Original-Facebook-Geek-Profile-Avatar-1.jpg" class=" img-responsive ">' +
                    '</div>' +
                '</div>';

    $('.msg_container_base').append(message);

    };
    
    var d = $('.msg_container_base').get(0);
    d.scrollTop = d.scrollHeight;

};

websocket.onclose = function() {
    websocket.send("disconnect");   
}
// Call onopen directly if socket is already open
if (websocket.readyState == WebSocket.OPEN) websocket.onopen();

$(document).on('click', '#btn-chat', function (e) {
    var message = $('#btn-input').val();
    websocket.send(message);
    $('#btn-input').val('');

});

$(document).on('click', '#chat-button', function (e) {
    $('#chat_window_1').toggleClass('hidden')
});

$(document).on('click', '.panel-heading span.icon_minim', function (e) {
    var $this = $(this);
    if (!$this.hasClass('panel-collapsed')) {
        $this.parents('.panel').find('.panel-body').slideUp();
        $this.addClass('panel-collapsed');
        $this.removeClass('glyphicon-minus').addClass('glyphicon-plus');
    } else {
        $this.parents('.panel').find('.panel-body').slideDown();
        $this.removeClass('panel-collapsed');
        $this.removeClass('glyphicon-plus').addClass('glyphicon-minus');
    }
});
$(document).on('focus', '.panel-footer input.chat_input', function (e) {
    var $this = $(this);
    if ($('#minim_chat_window').hasClass('panel-collapsed')) {
        $this.parents('.panel').find('.panel-body').slideDown();
        $('#minim_chat_window').removeClass('panel-collapsed');
        $('#minim_chat_window').removeClass('glyphicon-plus').addClass('glyphicon-minus');
    }
});
$(document).on('click', '#new_chat', function (e) {
    var size = $( ".chat-window:last-child" ).css("margin-left");
     size_total = parseInt(size) + 400;
    alert(size_total);
    var clone = $( "#chat_window_1" ).clone().appendTo( ".container" );
    clone.css("margin-left", size_total);
});
$(document).on('click', '.icon_close', function (e) {
    //$(this).parent().parent().parent().parent().remove();
    $( "#chat_window_1" ).remove();
    $( "#chat-button" ).remove();

});
};