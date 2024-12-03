import { WORDS } from './wordlist.js'

function scrollToBottom() {
    console.log("areeee")
    var chatContainer = document.querySelector(".messages");
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
window.onload = (event) => {
    scrollToBottom()
};
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
document.getElementById('message-input').addEventListener('submit', function(event){
	event.preventDefault();
    // console.log("🪼⋆｡𖦹°", event.target.querySelector('textarea').value)
    // console.log("🪼⋆｡𖦹°", )
    // const message = document.getElementById('msg').value;
    socket.send(
        JSON.stringify({
            'message': event.target.querySelector('#typed-message').value,
            'chat_name': `${chat_name}`,
            'sender': `${user_logged_in}`,
        })
    );
});



const wordleForm = document.querySelector('#wordle-form');
wordleForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const inputWord = document.querySelector('#word-input').value
    if (inputWord.length != 5) {
        alert("Word must be of length 5!")
        return
    }
    if (WORDS.includes(inputWord)) {
        fetch('/games/wordle/create_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ word: inputWord })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("WordleGame created successfully:", data.game);
                socket.send(
                    JSON.stringify({
                        'message': `[WORDLE]${data.game}`,
                        'chat_name': `${chat_name}`,
                        'sender': `${user_logged_in}`,
                }));
                alert("Wordle created successfully!")
            } else {
                console.error("Failed to create WordleGame:", data.error);
            }
        })
        .catch(error => console.error("Error:", error));
    } else {
        alert("INVALID WORD")
    }
})

var buffer = "@@@@";
var messageCount = 0;

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
        document.getElementById('typed-message').value = '';
    }

    // Here's where we append the message to the chatbox.
    var messageDiv = document.querySelector('.messages');
    console.log("BufferVal: " + buffer);

    let messageHTML = ``;
    if (message.includes('[WORDLE]'))
        messageHTML = `<a href='/games/wordle/${message.slice(8)}'>Guess my Wordle!</a>`
    else 
        messageHTML = `<p>${message}</p>`

    if (sender != user_logged_in) { 
        if(buffer == sender){
            messageDiv.innerHTML +=  
            `
            <div class="message_body" id="chatno${messageCount}">
            <div class="pfp" style="background-image: url('https://cmsassets.rgpub.io/sanity/images/dsfx7636/news_live/25497918317b8cb2029e51cc6c76c3bdfc91b702-1920x1133.jpg');"></div>
            <div class="flex_message">
              <div class="bubble sender">
                ${messageHTML}
              </div>
            </div>
          </div>
          `

            chat = "chatno"+(messageCount-1);
            console.log("Changing chat:" + chat);

            var hasNoPfp = document.getElementById(chat).getElementsByClassName("pfp");

            if(hasNoPfp.length > 0){
                document.getElementById(chat).getElementsByClassName("pfp")[0].removeAttribute("style");
                document.getElementById(chat).getElementsByClassName("pfp")[0].className = "empty_image";
            }
                
        }else{
            let messageHTML = ``;
            if (message.includes('[WORDLE]'))
                messageHTML = `<a href='/games/wordle/${message.slice(8)}'>Guess my Wordle!</a>`
            else 
                messageHTML = `<p>${message}</p>`

            messageDiv.innerHTML +=  
            `
            <div class="message_body" id="chatno${messageCount}">
                <div class="pfp" style="background-image: url('https://cmsassets.rgpub.io/sanity/images/dsfx7636/news_live/25497918317b8cb2029e51cc6c76c3bdfc91b702-1920x1133.jpg');"></div>
                <div class="flex_message">
                    <div class="chatter_name">
                        ${sender}
                    </div>
                    <div class="bubble sender">
                        ${messageHTML}
                    </div>
                </div>
            </div>
            `
        }
    } else {
        if (message.includes('[WORDLE]'))
            messageHTML = `<p>Guess my Wordle!</p>`
        else 
            messageHTML = `<p>${message}</p>`
        messageDiv.innerHTML += `
            <div class="bubble recipient">
                ${messageHTML}
            </div>`;
    }

    buffer = sender;
    messageCount++;
    scrollToBottom();
});

socket.onopen = (event) => {
    console.log("WebSocket connection opened!");
    const localStorageChatName = window.localStorage.getItem('chatName')
    const guessCount = window.localStorage.getItem('guessCount')
    if (chat_name == localStorageChatName
        && guessCount != 0) {
            console.log("HERE")
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(
                JSON.stringify({
                    'message': `I guessed your word in ${guessCount} ${guessCount==1? 'try':'tries'}`,
                    'chat_name': chat_name,
                    'sender': user_logged_in,
                })
            );

            window.localStorage.setItem('guessCount', 0);
        } else {
            console.error("WebSocket is not open.");
        }
        // socket.send(
        // JSON.stringify({
        //     'message': `I guessed your word in ${guessCount}`,
        //     'chat_name': `${chat_name}`,
        //     'sender': `${user_logged_in}`,
        // })
        // );
        // window.localStorage.setItem('guessCount', 0)
    }
};

socket.onclose = (event) => {
    console.log("WebSocket connection closed!");
};

