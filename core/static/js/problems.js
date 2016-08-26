function fix_tab_height(num) {
    var height = Math.max($('#problem'+num).height(),$('#hint'+num).height());
    $('#problem'+num).height(height);
    $('#hint'+num).height(height);
    $('#updates'+num).height(Math.max($('#updates'+num).height(), height));
}

function submit_problem(num) {
    $.ajax({
        url : "submit_problem/",
        type : "POST",
        data : {
            "problem": num,
            "guess" : $('#guess'+num.toString()).val()
        },

        success : function(json) {
            var icon, message;

            switch (json.alert) {
                case "already_solved":
                    message = "<strong>Hmm?</strong> You've already solved this.";
                    icon = "glyphicon glyphicon-info-sign";
                    break;
                case "correct":
                    message = "<strong>Good job!</strong> You've solved " + problem.title.strip() + "! (+" + str(problem.value) + " points)";
                    icon = "glyphicon glyphicon-ok-sign";
                    break;
                case "incorrect":
                    message = "<strong>Sorry.</strong> That was incorrect.";
                    break;
                case "incorrect_tried":
                    message = "<strong>Oops!</strong> You've already tried this solution.";
                    icon = "glyphicon glyphicon-remove-sign";
                    break;
            }

            $.notify({
                icon: icon,
                message: message
            }, {
                type: 'info',
                animate: {
	            	enter: 'animated fadeInRight',
	            	exit: 'animated fadeOutRight'
	            }
            });

            $('#outer'+num.toString()).html(json.html);
            fix_tab_height(num);

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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(window).load(function() {
    $.each($('.problem'), function (i,problem) {
        fix_tab_height(parseInt(problem.id.substr(5)));
    });
});