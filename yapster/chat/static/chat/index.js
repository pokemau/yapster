const closeUserDetail = document.querySelector("#close-icon");

closeUserDetail.addEventListener("click", () => {
	document.querySelector("#right-sidebar").style.display = "none";
});

async function loadUserDetails(userId) {
	try {
		const response = await fetch(`/chat/user-details/${userId}/`, {
			method: "GET",
			headers: {
				"X-Requested-With": "XMLHttpRequest",
			},
		});

		const data = await response.json();

		console.log(data);

		if (data.success) {
			document.querySelector("#right-sidebar p").textContent = data.first_name;
			document.querySelector("#right-username p").textContent = `@${data.username}`;
			document.querySelector("#right-bio p").textContent = data.bio || "No bio available";
			document.querySelector("#right-sidebar").style.display = "block";

			const addFriend = document.querySelector("#add-friend");
			const blockUser = document.querySelector("#block-user");

			if (data.you_are_blocked) {
				const userOptionsCont = document.querySelector("#user-options-cont");
				userOptionsCont.innerHTML = `
				<p>This user is unavailable</p>
				`;
				return;
			}

			if (data.is_blocked) {
				blockUser.textContent = "Unblock User";
				blockUser.setAttribute("href", `/friend/unblock_user/${data.id}`);
				addFriend.style.display = "none";
			} else {
				blockUser.textContent = "Block User";
				blockUser.setAttribute("href", `/friend/block_user/${data.id}`);
			}

			if (data.friend_request_active) {
				addFriend.textContent = "Cancel Friend Request";
				addFriend.setAttribute("href", `/friend/cancel_friend_request/${data.id}`);
			} else if (!data.is_friend) {
				addFriend.textContent = "Add Friend";
				addFriend.setAttribute("href", `/friend/friend_request/${data.id}`);
			} else {
				addFriend.textContent = "Remove Friend";
				addFriend.setAttribute("href", `/friend/remove_friend/${data.id}`);
			}
		}
	} catch (error) {
		console.error(error);
	}
}
/*
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
    const messageData = JSON.parse(event.data)['response_data'];
    
    var sender = messageData['sender'];
    var message = messageData['message'];
    
    console.log("sender: ", sender);
    console.log("message: ", message);
    // empty message input field after message has been sent
    if (sender == '{{user}}'){
        document.getElementById('msg').value = '';
    }

    //Basin naa diri ang double send
    // Here's where we append the message to the chatbox.
    var messageDiv = document.querySelector('.message');
    if (sender != '{{user}}') { // assuming you have a variable `currentUser` to hold the current user's name
        messageDiv.innerHTML += '<div class="receive"><p style="color: #000;">' + message + '<strong>-' + sender + '</strong></p></div>';
    } else {
        messageDiv.innerHTML += '<div class="send"><p style="color: #FF0000;">' + message + '</p></div>';
    }
    // scrollToBottom();
});

socket.onopen = (event) => {
    console.log("WebSocket connection opened!");
};

socket.onclose = (event) => {
    console.log("WebSocket connection closed!");
};
*/
