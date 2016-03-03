function login() {
    window.location.href = './login';
}

(function($) {
    $.QueryString = (function(a) {
        if (a == "") return {};
        var b = {};
        for (var i = 0; i < a.length; ++i)
        {
            var p=a[i].split('=');
            if (p.length != 2) continue;
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }
        return b;
    })(window.location.search.substr(1).split('&'))
})(jQuery);


window.onload = function () {
    var error_msg = $.QueryString["error_msg"];
    if (error_msg) {
        $("#error_msg").addClass('text-danger');
        $("#error_msg").text("Error: " + error_msg);
    }
}
