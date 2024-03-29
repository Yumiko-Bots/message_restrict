function fetchMessage() {
    var link = document.getElementById('message-link').value;
    if (!link.trim().startsWith('https://') && !link.trim().startsWith('http://') && !link.trim().startsWith('t.me')) {
        alert('Please enter a valid message link starting with "https", "http", or "t.me".');
        return;
    }
    fetch('/get_channel_content', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'channelUsername': link,
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('message-container').innerHTML = `
                    <h2>Message Content</h2>
                    <p>${data.messageContent}</p>
                    <h2>Photos</h2>
                    <ul>
                        ${data.photos.map(photo => `<li>${photo}</li>`).join('')}
                    </ul>
                `;
            } else {
                alert(`Failed to fetch message. Error: ${data.errorMessage}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while fetching the message.');
        });
}
