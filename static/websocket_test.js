const ws = new WebSocket("ws://localhost:8000/ws");

function connection(event) {
    event.preventDefault(); //don't use default event
    let mail = document.getElementById("mail");
    let password = document.getElementById("password");
    let input = {
        "id" : "connection",
        "mail" : mail.value,
        "password" : password.value
    };
    ws.send(JSON.stringify(input));
}

function accountCreation(event) {
    event.preventDefault(); //don't use default event
    let pseudonym = document.getElementById("pseudonym");
    let mail = document.getElementById("mailCreation");
    let password = document.getElementById("passwordCreation");
    let birthDate = document.getElementById("birthDate") 
    let input = {
        "id" : "accountCreation",
        "pseudonym" : pseudonym.value,
        "mail" : mail.value,
        "password" : password.value,
        "birthDate" : birthDate.value
    };
    console.log("creation account")
    ws.send(JSON.stringify(input));
}

// connection event
ws.onopen = () => {
    console.log('Connected at the websocket');
};

// close connection event
ws.onclose = (event) => {
    console.log('Disconnected at the websocket', event);
}

// handle reception messages
ws.onmessage = (event) => {
    let message = JSON.parse(event.data);
    console.log('from the back for', message["id"] + '\n', message["message"]);
};