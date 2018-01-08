/*
These functions are in a certain order on purpose. update() is the most important, and is called first. Please see http://blog.evilgeniustech.com/casparcg-html-producer-basics/ for more information.
*/

//This function is designed to update any information and get the animation ready to play
function update(arg) { //the key/value pairs configured in CasparCG client are passed here
    json = JSON.parse(arg); //You must parse the JSON string. I recommend storing the JSON outside this function so the parameters can be accessed by other functions
    
    //in this case, if we're passed a parameter called "f0" we want to change the text box accordingly. If not, we want it to say "hello world"
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
	}
    
    //Now that's all we have to do, fading in the box is handled by the play() function
}

//This function actually plays the animation that we've updated/configured with update()
function play(arg) {
    //in this case we just have to fade in a simple <div>
    $(".textbox").fadeTo(400, 1); // over 400ms, set opacity to 1
}

function stop() {
    $(".textbox").fadeTo(400, 0);
}

//This is an opportunity to smoothly transition out, so in this case we want to fade out our text
function next() {
    $(".textbox").fadeTo(400, 0);
}
