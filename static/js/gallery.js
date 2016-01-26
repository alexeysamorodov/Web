var SRC_PREFIX = '/static/images/photo/big/0';

function my_getCookie()
{
    if(!window.location.hash && getCookie('fav_image'))
    {
        var src = getCookie('fav_image');
        var idx = src[src.length - 5];
        window.location.hash = idx;
    }
    window.onhashchange = hashHandler;
    hashHandler();
    document.getElementById("right_button_a").onclick =
        dispatchDefaultHandler(function(){change_image(1)});
    document.getElementById("left_button_a").onclick =
        dispatchDefaultHandler(function(){change_image(-1)});
    document.getElementById("star_button_a").onclick =
        dispatchDefaultHandler(function(){fix_image()});
}

function hashHandler() {
    var curIdx = window.location.hash.slice(1);
    console.log(curIdx);
    if(curIdx == 'hide') {
        close_window();
    } else if(curIdx) {
        var src = SRC_PREFIX + curIdx + '.png';
        show_image(src);
    }
}

function fix_image() {
    var container = document.getElementById('imageContainer')
    var images = container.getElementsByTagName('img');
    var img_src;
    img_src = images[0].src;
    if (img_src.slice(-23) != getCookie('fav_image'))
    {
        deleteCookie('fav_image');
        setCookie('fav_image', img_src.slice(-23));
    }
    else
    {
        deleteCookie('fav_image');
    }
}

function preloading(src)
{
    var preload_img = new Image();
    preload_img.src = src;
}

function show_image(src) {
    document.getElementById("window_back").style.visibility = "visible";
    var container = document.getElementById('imageContainer');
    var images = container.getElementsByTagName('img');
    while(images.length > 0) {
        container.removeChild(images[0]);
    }
    document.getElementById("backer_help").style.visibility = "hidden";
    var loader = new Image();
    loader.src = '/static/images/loading.gif';
    container.appendChild(loader);
    var img = new Image();
    //img.style.visibility = "hidden";
    img.src = src;
    img.onload = function() {
        try { container.removeChild(loader); } catch(e) {}
        //img.style.visibility = "visible";
        var curIdx = parseInt(src[src.length - 5]);
        var nextIdx = curIdx != 9 ? curIdx + 1 : 1;
        var prevIdx = curIdx != 1 ? curIdx - 1 : 9;
        var nextUrl = src.slice(0, -5) + nextIdx + src.slice(-4);
        var prevUrl = src.slice(0, -5) + prevIdx + src.slice(-4);
        preloading(nextUrl);
        preloading(prevUrl);
    };
    container.appendChild(img);
}

document.onkeydown = function(e) {
    e = e || window.event;
    if (e.keyCode == 27)
    {
        if (document.getElementById("window_back").style.visibility == "visible") {

            {
                if (document.getElementById("backer_help").style.visibility == "hidden") {
                    window.location.hash = 'hide';
                }
                else {
                    close_helper();
                }
            }
        }
        else
        {
            if(document.getElementById("backer_help").style.visibility != "hidden")
            {
                close_helper();
            }
        }
    }
    if (e.keyCode == 112){
        if(e.stopPropagation) e.stopPropagation();
        else e.cancelBubble = true;
        if (document.getElementById("backer_help").style.visibility == "visible"){
            close_helper();
        }
        else {
            show_helper();
        }
        return false;
    }
    if (document.getElementById("window_back").style.visibility == "visible")
    {
        if (e.keyCode == 39)
        {
            change_image(1);
        }
        if (e.keyCode == 37)
        {
            change_image(-1);
        }
    }
}

function dispatchDefaultHandler(f) {
    return function(e) {
        if(e.stopPropagation) e.stopPropagation();
        else e.cancelBubble = true;
        f();
        return false;
    }
}


function deleteCookie(name) {
    setCookie(name, "", {
        expires: -1
    })
}
function setCookie(name, value, expires, path, domain, secure) {
    document.cookie = name + "=" + escape(value) +
        ((expires) ? "; expires=" + expires : "") +
        ((path) ? "; path=" + path : "") +
        ((domain) ? "; domain=" + domain : "") +
        ((secure) ? "; secure" : "");
}
function getCookie(name) {
    var cookie = " " + document.cookie;
    var search = " " + name + "=";
    var setStr = null;
    var offset = 0;
    var end = 0;
    if (cookie.length > 0) {
        offset = cookie.indexOf(search);
        if (offset != -1) {
            offset += search.length;
            end = cookie.indexOf(";", offset)
            if (end == -1) {
                end = cookie.length;
            }
            setStr = unescape(cookie.substring(offset, end));
        }
    }
    return(setStr);
}

function change_image(side) {
    var curIdx = parseInt(window.location.hash.slice(1));
    if(side == 1) {
        var nextIdx = curIdx != 9 ? curIdx + 1 : 1;
        window.location.hash = "" + nextIdx;
    } else {
        var prevIdx = curIdx != 1 ? curIdx - 1 : 9;
        window.location.hash = "" + prevIdx;
    }
}
function show_helper()
{
    document.getElementById("backer_help").style.visibility = "visible";
}
function close_helper()
{
    document.getElementById("backer_help").style.visibility = "hidden";
}
function close_window()
{
    var container = document.getElementById('imageContainer')
    var images = container.getElementsByTagName('img');
    for (var i = 0; i < images.length; i++)(function(i) {
        container.removeChild(images[i]);
    }(i))
    document.getElementById("window_back").style.visibility = "hidden";
}