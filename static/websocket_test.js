const ws = new WebSocket("ws://localhost:8000/ws");
let Token = document.cookie

const easymde = new EasyMDE({
    toolbar: [
        "bold",
        "italic",
        "heading",
        "|",
        {
        name: "save",
        action: function customSaveButton(editor) {
            const fileName = prompt("Veuillez saisir un nom de fichier :", "document1");
            document.getElementById("file_title").textContent = fileName.trim();
            saveDocument(fileName, editor.value())
            alert("Contenu sauvegardé : " + editor.value());
        },
        className: "fa fa-save",
        title: "Sauvegarder",
        },
    ],
    element: document.getElementById('markdown-editor'),
    autofocus: true,
    autosave: {
        enabled: true,
        uniqueId: "AutoSavedMarkdown",
        text: "Autosaved: ",
    },
    tabSize: 4,
    lineNumbers: true,
    sideBySideFullscreen: false,
});


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
};

function testConnection(event) {
    event.preventDefault(); //don't use default event
    let input = {
        "id" : "testConnection",
        "Token" : Token
    };
    ws.send(JSON.stringify(input));
};

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
};

function accountDelete(event) {
    event.preventDefault(); //don't use default event
    let pseudonym = document.getElementById("pseudonymDelete");
    let password = document.getElementById("passwordDelete");
    let input = {
        "id" : "accountDelete",
        "pseudonym" : pseudonym.value,
        "password" : password.value
    };
    console.log("delete account")
    ws.send(JSON.stringify(input));
};

function saveDocument(fileName, data) {
    let type = "md";
    let input = {
        "id" : "saveDocument",
        "Token" : Token,
        "name" : fileName,
        "type" : type,
        "data" : data,
        "is_new" : true
    };
    console.log("save document");
    ws.send(JSON.stringify(input));
};

function retrive_doc(button=null) {
    if (button) {
        let row = button.parentNode.parentNode;
        var input = {
            "id" : "retrive_doc",
            "Token" : Token,
            "name" : row.dataset.nom
        }
        title = document.getElementById("file_title")
        title.textContent = row.dataset.nom
    }
    else {
        var input = {
            "id" : "retrive_doc",
            "Token" : Token,
            "name" : ""
        }
    }
    console.log("retrive documents");
    ws.send(JSON.stringify(input));
};

function set_doc(documents) {
    let table = document.getElementById("doc_list");
    for(let row of documents){
        let new_row = table.insertRow(table.rows.length);
        let cell_nom = new_row.insertCell(0);
        let cell_actions = new_row.insertCell(1);
        cell_nom.innerHTML = row;
        cell_actions.innerHTML = '<button onclick="retrive_doc(this)">edit</button>';
        new_row.dataset.nom = row;
    }
};

// connection event
ws.onopen = () => {
    console.log('Connected at the websocket');
};

// close connection event
ws.onclose = (event) => {
    console.log('Disconnected at the websocket');
};

// handle reception messages
ws.onmessage = (event) => {
    let message = JSON.parse(event.data);
    console.log('from the back for', message["id"] + '\n', message["message"]);
    if (message["id"] == "connection"){
        Token = message["message"]["Token"];
        document.cookie = Token;
        retrive_doc();
    }
    if (message["id"] == "retrive_doc"){
        if (typeof message["message"] === typeof [] ){
            set_doc(message["message"]);
        }
        else{
            if (easymde !== null){
                console.log(document.getElementById('markdown-editor'))
                easymde.value(message["message"]);
            }
        }
    }
};