function change_password() {
    $.ajax({
        url : "change_password/",
        type : "POST",
        data : {
            "old": $("#id_password").val(),
            "new": $("#id_new_password").val(),
            "confirm": $("#id_confirm_password").val()
        },

        success : function(json) {
            $.notify({
                icon: json.alert_class,
                message: json.alert
            }, {
                type: json.alert_type,
                animate: {
	            	enter: 'animated fadeInRight',
	            	exit: 'animated fadeOutRight'
	            }
            });

            $("#id_password").val('');
            $("#id_new_password").val('');
            $("#id_confirm_password").val('');
        },

        error : function(xhr,errmsg,err) {
            alert(errmsg + ". " + xhr.status + ": " + xhr.responseText);
        }
    });
};

function check_press(e) {
    if (e.which == 13) change_password();
}