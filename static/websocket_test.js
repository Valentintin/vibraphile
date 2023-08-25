const ws = new WebSocket("ws://localhost:8000/ws");
let Token = document.cookie

const easymde = new EasyMDE({
    toolbar: [
        "heading",
        "bold",
        "italic",
        "quote",
        "unordered-list",
        "ordered-list",
        "table",
        "link",
        "image",
        "upload-image",
        "|",
        "undo",
        "redo",
        "side-by-side",
        "fullscreen",
        "|",
        {
            name: "save",
            action: function customSaveButton(editor) {
                if (document.getElementById("file_title").textContent === "untilted.md"){
                    var fileName = prompt("Veuillez saisir un nom de fichier :", "document1");
                    document.getElementById("file_title").textContent = fileName.trim();
                }
                else {
                    var fileName = document.getElementById("file_title").textContent
                }
                saveDocument(fileName, editor.value())
                alert("Contenu sauvegardé : " + editor.value());
            },
            
            className: "fa fa-save",
            title: "Sauvegarder",
        },
        {
            name: "new doc",
            action: function customeNewDocButton(editor) {
                document.getElementById("file_title").textContent = "untilted.md"
                editor.value("")
            },
            
            className: "fa fa-file-text",
            title: "create a new doc",
        },
        "guide",
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
    let mail = document.getElementById("mailConnection");
    let password = document.getElementById("passwordConnection");
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

function modify(infoModify) {
    let modification = document.getElementById(infoModify);
    let input = {
        "id" : "modifyAccount",
        "Token" : Token,
        "infoModify" : infoModify,
        "modification" : modification.value
    };
    console.log("modify account info");
    if (infoModify !== "password"){
        let label = document.querySelector("label[for='" + infoModify + "']");
        label.textContent = "actual "+infoModify+" : "+modification.value
    }
    ws.send(JSON.stringify(input));
}

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

function retriveDoc(button=null) {
    if (button) {
        let row = button.parentNode.parentNode;
        var input = {
            "id" : "retriveDoc",
            "Token" : Token,
            "name" : row.dataset.nom
        }
        title = document.getElementById("file_title")
        title.textContent = row.dataset.nom
    }
    else {
        var input = {
            "id" : "retriveDoc",
            "Token" : Token,
            "name" : ""
        }
    }
    console.log("retrive documents");
    ws.send(JSON.stringify(input));
};

function setDoc(documents) {
    let table = document.getElementById("doc_list");
    for(let row of documents){
        let new_row = table.insertRow(table.rows.length);
        let cell_nom = new_row.insertCell(0);
        let cell_actions = new_row.insertCell(1);
        cell_nom.innerHTML = row;
        cell_actions.innerHTML = '<button onclick="retriveDoc(this)">edit</button>';
        new_row.dataset.nom = row;
    }
};

// connection event
ws.onopen = () => {
    console.log('Connected at the websocket');
};

// close connection event
ws.onclose = () => {
    console.log('Disconnected at the websocket');
};

// handle reception messages
ws.onmessage = (event) => {
    let message = JSON.parse(event.data);
    console.log('from the back for', message["id"] + '\n', message["message"]);
    if (message["id"] == "connection"){
        Token = message["message"]["Token"];
        if(Token !== undefined){
            document.cookie = Token;
            retriveDoc();
        }
    }
    if (message["id"] == "retriveDoc"){
        if (typeof(message["message"]) === typeof([]) ){
            setDoc(message["message"]);
        }
        else{
            if (easymde !== null){
                console.log(document.getElementById('markdown-editor'))
                easymde.value(message["message"]);
            }
        }
    }
};