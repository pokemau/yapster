let selectedUsers = []; // Store selected users

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

	loadChat(userId)
}

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
	.catch(error => console.error("Error:", error));
}

function toggleDropdown(element) {
  const dropdown = element.parentElement;
  dropdown.classList.toggle('show');
}

// Function to filter and display users based on query
function filterUsers(query) {
    const usersCont = document.getElementById("users-cont");
    if (!query) {
        usersCont.innerHTML = ""; // Clear queried users if input is empty
        return;
    }
	
    // Perform AJAX request to fetch users based on query
    fetch(`/chat/query_stuff/query_users/?gc_query=${encodeURIComponent(query)}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
			"X-CSRFToken": csrfToken,
            "X-Requested-With": "XMLHttpRequest",
        },
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Failed to fetch users:  ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.users && data.users.length > 0) {
                // Populate the users container
                usersCont.innerHTML = data.users
                    .map(
                        (user) => `
                    <div class="user" onclick="addUser('${user.id}', '${user.first_name}', '${user.last_name}')">
                        <div class="left-profile-pic"></div>
                        <div class="name-time-msg">
                            <div class="name-time">
                                <p class="name">${user.first_name} ${user.last_name}</p>
                                <p class="time-sent">@${user.username}</p>
                            </div>
                        </div>
                    </div>
                `
                    )
                    .join("");
            } else {
                usersCont.innerHTML = "<p>No users found.</p>";
            }
        })
        .catch((error) => console.error("Error fetching users:", error));
}

// Function to add a user to the selected names
function addUser(firstName, lastName) {
    const searchInput = document.getElementById("search-input");
    const usersCont = document.getElementById("users-cont");

    // Check if the user is already selected
    if (selectedUsers.some((user) => user.firstName === firstName && user.lastName === lastName)) {
        return;
    }

    // Add user to the selected list
    selectedUsers.push({ firstName, lastName });

    // Update the UI
    const selectedNames = document.getElementById("selected-names");
    const userDiv = document.createElement("div");
    userDiv.className = "selected-name";
    userDiv.innerHTML = `${firstName} ${lastName} 
        <span class="remove-name" onclick="removeUser('${firstName}', '${lastName}')">&times;</span>`;
    selectedNames.appendChild(userDiv);

    // Clear the search input and query results
    searchInput.value = "";
    usersCont.innerHTML = "";
}

// Function to remove a user from the selected names
function removeUser(firstName, lastName) {
    selectedUsers = selectedUsers.filter(
        (user) => user.firstName !== firstName || user.lastName !== lastName
    );

    // Update the UI
    const selectedNames = document.getElementById("selected-names");
    selectedNames.innerHTML = ""; // Clear all selected names
    selectedUsers.forEach((user) => {
        const userDiv = document.createElement("div");
        userDiv.className = "selected-name";
        userDiv.innerHTML = `${user.firstName} ${user.lastName} 
            <span class="remove-name" onclick="removeUser('${user.firstName}', '${user.lastName}')">&times;</span>`;
        selectedNames.appendChild(userDiv);
    });
}
