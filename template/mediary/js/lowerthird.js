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
		ss = 'linear-gradient(to right, '+hexToRgbA(json.fgcol,1)+', '+hexToRgbA(json.fgcol,0.2)+')';
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

function hexToRgbA(hex, alpha){
    var c;
    if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
        c= hex.substring(1).split('');
        if(c.length== 3){
            c= [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c= '0x'+c.join('');
        return 'rgba('+[(c>>16)&255, (c>>8)&255, c&255, alpha].join(',')+')';
    }
    throw new Error('Bad Hex');
}
