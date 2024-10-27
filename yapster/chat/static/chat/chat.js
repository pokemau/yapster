function scrollToBottom() {
    var chatContainer = document.getElementById("chatContainer");
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
// DO YOU WANT TO BUILD A SNOW MAN? :(
// Determine the WebSocket protocol based on the application's URL
const websocketProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const wsEndpoint = `${websocketProtocol}://${window.location.host}/ws/${chat_name}/`;
// Create a new WebSocket connection
const socket = new WebSocket(wsEndpoint);
// Successful connection event
socket.onopen = (event) => {
    console.log("WebSocket connection opened!");
};
// Socket disconnect event
socket.onclose = (event) => {
    console.log("WebSocket connection closed!");
};
// Form submit listener
document.getElementById('message-form').addEventListener('submit', function(event){
	event.preventDefault();
    // console.log("🪼⋆｡𖦹°", event.target.querySelector('textarea').value)
    // console.log("🪼⋆｡𖦹°", )
    // const message = document.getElementById('msg').value;
    socket.send(
        JSON.stringify({
            'message': event.target.querySelector('textarea').value,
            'chat_name': `${chat_name}`,
            'sender': `${user_logged_in}`,
        })
    );
});

        
// response from consumer on server
socket.addEventListener("message", (event) => {
	// event.preventDefault();
    const messageData = JSON.parse(event.data)['response_data'];
    
    var sender = messageData['sender'];
    var message = messageData['message'];
    
    console.log("sender: ", sender);
    console.log("message: ", message);
    // empty message input field after message has been sent
    if (sender == user_logged_in){
        document.getElementById('msg').value = '';
    }

    //Basin naa diri ang double send
    // Here's where we append the message to the chatbox.
    var messageDiv = document.querySelector('.messages');
    if (sender != user_logged_in) { 
        messageDiv.innerHTML += '<div class="receive"><p style="color: #000;">' + message + '<strong>-' + sender + '</strong></p></div>';
    } else {
        messageDiv.innerHTML += '<div class="send"><p>' + message + '</p></div>';
    }
    scrollToBottom();
});

socket.onopen = (event) => {
    console.log("WebSocket connection opened!");
};

socket.onclose = (event) => {
    console.log("WebSocket connection closed!");
};