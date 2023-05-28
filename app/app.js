console.log("Ok!!!")
function senddata() {
    let input_number = document.getElementById("input_number").value;
    let input_password = document.getElementById("input_password").value;
    document.getElementById("login_button");
    console.log(input_number, input_password);
}

function signup() {
    document.getElementById("signup");
    console.log("signup");
    window.location.href = "templates/signup.html";
}

function register() {
    document.getElementById("register");
    console.log("register");
}

function authgoogle(){
    document.getElementById("authgoogle");
    console.log("authgoogle");
}

function authfacebook(){
    document.getElementById("authfacebook");
    console.log("authfacebook");
}

function authapple(){
    document.getElementById("authapple");
    console.log("authapple");
}