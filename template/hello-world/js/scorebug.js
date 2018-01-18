/*
These functions are in a certain order on purpose. update() is the most important, and is called first. Please see http://blog.evilgeniustech.com/casparcg-html-producer-basics/ for more information.
*/

//This function is designed to update any information and get the animation ready to play
function update(arg) { //the key/value pairs configured in CasparCG client are passed here
    json = JSON.parse(arg); //You must parse the JSON string. I recommend storing the JSON outside this function so the parameters can be accessed by other functions
    
    //in this case, if we're passed a parameter called "f0" we want to change the text box accordingly. If not, we want it to say "hello world"
    if (json.team1 !== undefined) {
        $("#team1").html(json.team1);
    }
    if (json.team2 !== undefined) {
        $("#team2").html(json.team2);
    }
    if (json.score1 !== undefined) {
        $("#score1").html(json.score1);
    }
    if (json.score2 !== undefined) {
        $("#score2").html(json.score2);
    }

    if (json.team1bg !== undefined) {
        ss = 'linear-gradient(to bottom, '+hexToRGBA(json.team1bg, 0.5)+', '+hexToRGBA(json.team1bg,1)+')';
        $("#team1").css('background-image', ss);
    }
    if (json.team1fg !== undefined) {
        $("#team1").css('color', json.team1fg);
    }

    if (json.team2bg !== undefined) {
        ss = 'linear-gradient(to bottom, '+hexToRGBA(json.team2bg, 0.5)+', '+hexToRGBA(json.team2bg,1)+')';
        $("#team2").css('background-image', ss);
    }
    if (json.team2fg !== undefined) {
        $("#team2").css('color', json.team2fg);
    }
    if (json.fontsize !== undefined) {
        $(".scorebug").css('font-size', json.fontsize+'px');
    }

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

function hexToRGBA(hex, alpha){
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
