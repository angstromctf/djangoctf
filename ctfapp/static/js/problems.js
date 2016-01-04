function submit_problem(num) {
    $.ajax({
        url : "submit_problem/",
        type : "POST",
        data : {
            "problem": num,
            "guess" : $('#guess'+num.toString()).val()
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

            $('#outer'+num.toString()).html(json.html);

            $.ajax({
                url : "/score/",

                success : function(data) {
                    $('#score').html(data);
                },

                error : function(xhr,errmsg,err) {
                    alert(errmsg + ". " + xhr.status + ": " + xhr.responseText);
                }
            });
        },

        error : function(xhr,errmsg,err) {
            alert(errmsg + ". " + xhr.status + ": " + xhr.responseText);
        }
    });
};

function check_press(e, num) {
    if (e.which == 13) submit_problem(num);
}