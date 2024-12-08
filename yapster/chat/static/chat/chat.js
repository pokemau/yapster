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
const wsEndpoint = `${websocketProtocol}://${window.location.host}/ws/${currentChatID}/`;
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
            'sender_nickname': `${currentUserNickname}`,
            'current_chatID': `${currentChatID}`
        })
    );
    updateUI();
});


function updateUI() {
    const elem = document.querySelector('.user-option__a')
    if (elem)
        elem.style.display = 'none'
}

const wordleForm = document.querySelector('#wordle-form');
wordleForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const inputWord = document.querySelector('#word-input').value
    if (WORDS.includes(inputWord)) {
        console.log("VALID WORD");
        
        fetch('/games/wordle/create_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ word: inputWord, room: chat_name })
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
                        'sender_nickname': `${currentUserNickname}`,
                }));
                document.getElementById("myModal").style.display = 'none';
                document.querySelector('#word-input').value = '';
                updateUI()
            } else {
                console.error("Failed to create WordleGame:", data.error);
            }
        })
        .catch(error => console.error("Error:", error));
    } else {
        console.log("INVALID WORD")
    }
})
 
var messageCount = 0;
console.log("BufferVal: " + buffer);
var firstChat = true;

// response from consumer on server
socket.addEventListener("message", (event) => {
    
	// event.preventDefault();
    const messageData = JSON.parse(event.data)['response_data'];
    let chat = "";
    
    var sender = messageData['sender'];
    var sender_nickname = messageData['sender_nickname'];
    var message = messageData['message'];
    
    console.log("sender: ", sender);
    console.log("message: ", message);
    // empty message input field after message has been sent
    if (sender_nickname == currentUserNickname){
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

    if (messageData.system_message){
        messageDiv.innerHTML += `<div class="system-message"><p>${message}</p></div>`;
    }else{
        if (sender != user_logged_in) { 
            if(buffer == sender_nickname){
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
                if(!firstChat){
                    chat = "chatno"+(messageCount-1);
                    console.log("Changing chat:" + chat);
        
                    var hasNoPfp = document.getElementById(chat).getElementsByClassName("pfp");
        
                    console.log("Does it have pfp: " + hasNoPfp.length)
                }else{
                    chat = "prevchat"+(chatCounter);
                    console.log("Changing chat:" + chat);
        
                    var hasNoPfp = document.getElementById(chat).getElementsByClassName("pfp");
        
                    console.log("Does it have pfp: " + hasNoPfp.length)
                }

                
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
                            ${sender_nickname}
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
        scrollToBottom();
    }


    buffer = sender_nickname;
    messageCount++;
    firstChat = false;
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

document.addEventListener('DOMContentLoaded', function() {
    const editIcons = document.querySelectorAll('.edit-icon');

    editIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const nicknameItem = this.closest('.nickname-item');
            const nicknameSpan = nicknameItem.querySelector('.nickname');
            const editInput = nicknameItem.querySelector('.edit-nickname-input');
            const saveButton = nicknameItem.querySelector('.save-nickname-btn');

            nicknameSpan.style.display = 'none';
            editInput.style.display = 'block';
            saveButton.style.display = 'block';
            this.style.display = 'none';
            editInput.value = nicknameSpan.textContent.trim();
            editInput.focus();
            editInput.select();
        });
    });

    const saveButtons = document.querySelectorAll('.save-nickname-btn');
    saveButtons.forEach(button => {
        button.addEventListener('click', function() {
            const nicknameItem = this.closest('.nickname-item');
            const nicknameSpan = nicknameItem.querySelector('.nickname');
            const editInput = nicknameItem.querySelector('.edit-nickname-input');
            const editIcon = nicknameItem.querySelector('.edit-icon');

            const oldNickname = nicknameSpan.textContent.trim();
            const newNickname = editInput.value.trim();

            // Do nothing if the nickname hasn't changed
            if (oldNickname === newNickname) {
                nicknameSpan.style.display = 'block';
                editInput.style.display = 'none';
                this.style.display = 'none';
                editIcon.style.display = 'block';
                return;
            }

            // Optimistically update the UI
            nicknameSpan.textContent = newNickname;
            nicknameSpan.style.display = 'block';
            editInput.style.display = 'none';
            this.style.display = 'none';
            editIcon.style.display = 'block';

            // Send the updated nickname to the server
            const userId = nicknameItem.dataset.userId; // Assume `data-user-id` is set in each nickname-item div

            fetch(changeNicknameUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ user_id: userId, new_nickname: newNickname })
            })
                .then(response => response.json())
                .then(data => {
                    if (!data.success) {
                        // Handle errors and revert the UI
                        alert(data.error || "Failed to update nickname.");
                        console.log(csrfToken)
                        nicknameSpan.textContent = oldNickname;
                    }else if(data.success){
                        location.reload();
                    }
                })
                .catch(error => {
                    console.error("Error updating nickname:", error);
                    alert("An error occurred while updating the nickname.");
                    nicknameSpan.textContent = oldNickname;
                });
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const resetButtons = document.querySelectorAll('.reset-nickname-btn');

    resetButtons.forEach(button => {
        button.addEventListener('click', function () {
            const nicknameItem = this.closest('.nickname-item');
            const userId = nicknameItem.dataset.userId; // Ensure the div has a data attribute with user ID

            fetch(resetNicknameUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ user_id: userId }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const nicknameSpan = nicknameItem.querySelector('.nickname');
                        nicknameSpan.textContent = data.default_nickname;

                        const editInput = nicknameItem.querySelector('.edit-nickname-input');
                        if (editInput) {
                            editInput.value = data.default_nickname;
                        }

                        // alert("Nickname reset successfully!");
                        location.reload()
                    } else {
                        alert(data.error);
                    }
                })
                .catch(error => {
                    console.error("Error resetting nickname:", error);
                });
        });
    });
});



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
