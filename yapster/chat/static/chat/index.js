// closeUserDetail.addEventListener("click", () => {
// 	document.querySelector("#right-sidebar").style.display = "none";
// });

async function loadUserDetails(userId) {
	loadChat(userId)
	try {
		const response = await fetch(`/chat/user-details/${userId}/`, {
			method: "GET",
			headers: {
				"X-Requested-With": "XMLHttpRequest",
			},
		});

		const data = await response.json();

		console.log(data);

		// if (data.success) {
		// 	document.querySelector("#right-sidebar p").textContent = data.first_name;
		// 	document.querySelector("#right-username p").textContent = `@${data.username}`;
		// 	document.querySelector("#right-bio p").textContent = data.bio || "No bio available";
		// 	document.querySelector("#right-sidebar").style.display = "block";

		// 	const addFriend = document.querySelector("#add-friend");
		// 	const blockUser = document.querySelector("#block-user");

		// 	if (data.you_are_blocked) {
		// 		const userOptionsCont = document.querySelector("#user-options-cont");
		// 		userOptionsCont.innerHTML = `
		// 		<p>This user is unavailable</p>
		// 		`;
		// 		return;
		// 	}

		// 	if (data.is_blocked) {
		// 		blockUser.textContent = "Unblock User";
		// 		blockUser.setAttribute("href", `/friend/unblock_user/${data.id}`);
		// 		addFriend.style.display = "none";
		// 	} else {
		// 		blockUser.textContent = "Block User";
		// 		blockUser.setAttribute("href", `/friend/block_user/${data.id}`);
		// 	}

		// 	if (data.friend_request_active) {
		// 		addFriend.textContent = "Cancel Friend Request";
		// 		addFriend.setAttribute("href", `/friend/cancel_friend_request/${data.id}`);
		// 	} else if (!data.is_friend) {
		// 		addFriend.textContent = "Add Friend";
		// 		addFriend.setAttribute("href", `/friend/friend_request/${data.id}`);
		// 	} else {
		// 		addFriend.textContent = "Remove Friend";
		// 		addFriend.setAttribute("href", `/friend/remove_friend/${data.id}`);
		// 	}
		// }
	} catch (error) {
		console.error(error);
	}
}

// Gi load chat gamit user ids pang query then ang name kuhaon
function loadChat(...targetUserId) {
	const allUserIDs = [...targetUserId]
	
	fetch(getOrCreateChatUrl, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": csrfToken,
			'X-Requested-With': 'XMLHttpRequest'
		},
		body: JSON.stringify({ target_user_ids: allUserIDs})
	})
	.then(response => response.json())
	.then(data => {
		if (data.success) {
			window.location.href = `/chat/${data.chat_name}/`;
		} else {
			console.error("Error:", data.error);
		}
	})
		.catch((error) => console.error("Error:", error));
}

function loadChatWithID(chatId) {
    console.log("Loading chat with ID:", chatId);

    // Redirect the user to the chat URL based on the chat ID
    window.location.href = `/chat/${chatId}/`;
}

function toggleDropdown(element) {
  const dropdown = element.parentElement;
	dropdown.classList.toggle("show");
}

// Modal stuff
var modal = document.getElementById("myModal");
const btn = document.querySelector("#wordle-btn");
btn.addEventListener('click', () => {
  modal.style.display = "block";
})
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
		document.querySelector('#word-input').value = '';
  }
}
var span = document.getElementsByClassName("close")[0];
span.onclick = function() {
  modal.style.display = "none";
	document.querySelector('#word-input').value = '';
}
