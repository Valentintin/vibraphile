//This file create a interactive markdown's editor for the WebSite

var textarea = document.createElement('textarea');
textarea.id = 'markdown-editor';
document.body.appendChild(textarea);

const easymde = new EasyMDE({
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
