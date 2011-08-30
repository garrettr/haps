function random_char() {
    var chars = "0123456789!@#$%^&*()ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz";
    var rand = Math.floor(Math.random() * chars.length);
    return chars.charAt(rand);
}
function add_padding() {
    var padding_size = Math.floor(Math.random()*1572864)+524288; // between .5mb and 2mb
    var padding = '';
    for(var i=0; i<padding_size; i++) padding += random_char();
    var padding_field = document.getElementById('padding');
    padding_field.setAttribute('value', padding);
}
window.onload=add_padding;
