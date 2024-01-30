function createPaste() {
    const code = document.getElementById('code').value;
    fetch('/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `code=${encodeURIComponent(code)}`,
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = `/paste/${data.paste_id}`;
    });
}

function deletePaste(pasteId) {
    fetch(`/delete/${pasteId}`)
    .then(() => {
        window.location.reload();
    });
}
