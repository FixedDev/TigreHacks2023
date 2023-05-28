console.log("Ok!!!")
// post a /internal_login
// LoginResult.SUCCESS
// LoginResult.WRONG_PASSWORD
// LoginResult.USER_NOT_EXIST
// LoginResult.ERROR
function senddata() {
    let input_number = document.getElementById("input_number").value;
    let input_password = document.getElementById("input_password").value;

    const url = "http://localhost:5500/internal_login";
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
      })
        .then(response => response.json())
        .then(data => {
          // Maneja la respuesta del servidor
          console.log(data);
        })
        .catch(error => {
          // Maneja cualquier error de la petición
          console.error('Error:', error);
        });

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