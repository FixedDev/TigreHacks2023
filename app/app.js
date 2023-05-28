console.log("Ok!!!");
// post a /internal_login
// LoginResult.SUCCESS
// LoginResult.WRONG_PASSWORD
// LoginResult.USER_NOT_EXIST
// LoginResult.ERROR

// post a /internal_register
// {
//   "result": "RegisterResult.SUCCESS",
//   "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0NzMyZjgzNzhjODE3ODMyM2MzZmJmMCJ9.LkrTHrq3F8n7OrYVOB5pnUd7wbcoW2lddg57YZHom70"
// }
// en success devuelve eso
//
function senddata() {
    let input_number = document.getElementById("input_number").value;
    let input_password = document.getElementById("input_password").value;
    const path = "http://127.0.0.1:5000/internal_login";
    
    fetch(path)
    .then(res => res.json())
    .then(res => console.log(res));
    
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

function authgoogle() {
    document.getElementById("authgoogle");
    console.log("authgoogle");
}

function authfacebook() {
    document.getElementById("authfacebook");
    console.log("authfacebook");
}

function authapple() {
    document.getElementById("authapple");
    console.log("authapple");
}
