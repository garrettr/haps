function random_char() {
    var chars = "0123456789!@#$%^&*()ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
    var rand = Math.floor(Math.random() * chars.length);
    return chars.charAt(rand);
}
function add_padding() {
    // "loading" gif
    document.getElementById('notes').innerHTML = '<img src="/static/loading.gif" /><br/>Please wait, generating padding...';
    var padding_size = Math.floor(Math.random()*1572864)+524288; // between .5mb and 2mb
    var padding = '';

    var size_so_far = 0;
    var interval = setInterval(function() {
        for(var i=0; i<10000; i++) {
            padding += 'A';
            size_so_far++;
            if(size_so_far == padding_size) {
                clearInterval(interval);
                document.getElementById('padding').setAttribute('value', padding);
                document.getElementById('notes').innerHTML = 'Padding generation complete!';
                break;
            }
        }
    }, 0);
}
window.onload=function() { add_padding(); };
