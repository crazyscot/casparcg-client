function update(arg) {
    json = JSON.parse(arg);
    
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
        ss = 'linear-gradient(to bottom, '+hexToRGBA(json.team1bg, 0.9)+', '+hexToRGBA(json.team1bg,0.5)+')';
        $("#team1").css('background-image', ss);
    }
    if (json.team1fg !== undefined) {
        $("#team1").css('color', json.team1fg);
    }

    if (json.team2bg !== undefined) {
        ss = 'linear-gradient(to bottom, '+hexToRGBA(json.team2bg, 0.9)+', '+hexToRGBA(json.team2bg,0.5)+')';
        $("#team2").css('background-image', ss);
    }
    if (json.team2fg !== undefined) {
        $("#team2").css('color', json.team2fg);
    }
    if (json.fontsize !== undefined) {
        $(".scorebug").css('font-size', json.fontsize+'px');
    }
}

function play(arg) {
    $(".scorebug").fadeTo(400, 1); // over 400ms, set opacity to 1
}

function stop() {
    $(".scorebug").fadeTo(400, 0);
}

//This is an opportunity to smoothly transition out, so in this case we want to fade out our text
function next() {
    $(".scorebug").fadeTo(400, 0);
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
