$.getScript("js/common.js");

/*
These functions are in a certain order on purpose. update() is the most important, and is called first. Please see http://blog.evilgeniustech.com/casparcg-html-producer-basics/ for more information.
*/

function update(arg) {
    json = JSON.parse(arg);
    if (json.f0 !== undefined) {
        $("#f0").html(json.f0);
    }
    if (json.f1 !== undefined) {
        $("#f1").html(json.f1);
    }
	
	if (json.bgcol !== undefined) {
		$(".textbox").css('background-color', json.bgcol);
	}
	if (json.fgcol !== undefined) {
		$('.textbox').css('color', json.fgcol);
		ss = 'linear-gradient(to right, '+hex2RGBA(json.fgcol,1)+', '+hex2RGBA(json.fgcol,0.2)+')';
		$('hr').css('background-image', ss);
	}
}

function play(arg) {
    $(".textbox").fadeTo(400, 1); // over 400ms, set opacity to 1
}

function stop() {
    $(".textbox").fadeTo(400, 0);
}

//This is an opportunity to smoothly transition out, so in this case we want to fade out our text
function next() {
    $(".textbox").fadeTo(400, 0);
}
