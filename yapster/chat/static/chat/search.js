let isCreateChatState = false; // Tracks the state of the search bar
let selectedUsers = []; // Stores selected users in create-chat state

function toggleCreateChatState() {
    isCreateChatState = !isCreateChatState;

    // Update UI based on the state
    const selectedNames = document.getElementById("selected-names");
    const searchInput = document.getElementById("search-input");
    const exitButton = document.getElementById("exit-create-chat"); // Exit button
    const chatList = document.getElementById("chat-list"); // Existing chats
    const searchResults = document.getElementById("search-results"); // Queried users
    const currentChats = document.getElementById("current-chats"); // Current user's chats
    const createChatButton = document.querySelector(".chat-create"); // Create GC button

    if (isCreateChatState) {
        selectedNames.style.display = "flex"; // Show selected names container
        searchInput.placeholder = "Add users to group...";
        searchInput.value = ""; // Clear input for new search
        if (exitButton) exitButton.style.display = "inline"; // Show exit button
        if (chatList) chatList.style.display = "none"; // Hide existing chats
        if (searchResults) searchResults.innerHTML = ""; // Clear search results
        if (currentChats) currentChats.style.display = "none"; // Hide current chats

        // Change button functionality to finalize group creation
        createChatButton.textContent = "Create GC";
        createChatButton.onclick = createGroupChat;
    } else {
        selectedNames.style.display = "none"; // Hide selected names container
        selectedUsers = []; // Clear selected users
        selectedNames.innerHTML = ""; // Clear capsules
        searchInput.placeholder = "Search chats or users...";
        searchInput.value = ""; // Clear input
        if (exitButton) exitButton.style.display = "none"; // Hide exit button
        if (chatList) chatList.style.display = "block"; // Show existing chats
        if (searchResults) searchResults.innerHTML = ""; // Clear search results
        if (currentChats) currentChats.style.display = "block"; // Show current chats

        // Restore button functionality to toggle Create GC state
        createChatButton.textContent = "Create Chat";
        createChatButton.onclick = toggleCreateChatState;
    }
}

// Finalize group creation
function createGroupChat() {
    if (selectedUsers.length === 0) {
        alert("Please add at least one user to create a group chat.");
        return;
    }

    // Extract user IDs and call loadChat with them
    const userIds = selectedUsers.map((user) => user.id);
    loadChat(...userIds); // Call the function with selected user IDs
}

// Handles input in the search bar
function handleSearchInput(query) {
    const searchResults = document.getElementById("search-results");
    const currentChats = document.getElementById("current-chats");

    if (query) {
        searchResults.style.display = "block"; // Show search results
        if (currentChats) currentChats.style.display = "none"; // Hide current chats during search
    } else {
        searchResults.style.display = "none"; // Hide search results when empty
        if (!isCreateChatState && currentChats) currentChats.style.display = "block"; // Show current chats in default state
    }

    if (isCreateChatState) {
        filterUsers(query, true);
    } else {
        filterUsers(query, false);
    }
}

// Function to filter users or chats based on query
function filterUsers(query, isAddingToGroup) {
    const searchResults = document.getElementById("search-results");
    const chatList = document.getElementById("chat-list");

    if (!query) {
        if (!isAddingToGroup) {
            if (chatList) chatList.style.display = "block"; // Show existing chats in default state
        }
        if (searchResults) searchResults.style.display = "none"; // Hide search results
        return;
    }

    // Fetch search results via AJAX
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
                throw new Error(`Failed to fetch users: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.users && data.users.length > 0) {
                if (searchResults) {
                    searchResults.style.display = "block";
                    searchResults.innerHTML = data.users
                        .map((user) => {
                            if (isAddingToGroup) {
                                return `
                                    <div class="user" onclick="addUser('${user.id}', '${user.first_name}', '${user.last_name}')">
                                        <div class="left-profile-pic"></div>
                                        <div class="name-time-msg">
                                            <p class="name">${user.first_name} ${user.last_name}</p>
                                            <p class="time-sent">@${user.username}</p>
                                        </div>
                                    </div>
                                `;
                            } else {
                                return `
                                    <div class="user" onclick="loadUserDetails(${user.id})">
                                        <div class="left-profile-pic"></div>
                                        <div class="name-time-msg">
                                            <p class="name">${user.first_name} ${user.last_name}</p>
                                            <p class="time-sent">@${user.username}</p>
                                        </div>
                                    </div>
                                `;
                            }
                        })
                        .join("");
                }
                if (chatList) chatList.style.display = "none"; // Hide chats during search
            } else {
                if (searchResults) searchResults.innerHTML = "<p>No users found.</p>";
            }
        })
        .catch((error) => console.error("Error fetching users:", error));
}

// Adds a user to the selected users list in create-chat state
function addUser(userId, firstName, lastName) {
    if (selectedUsers.find((user) => user.id === userId)) return; // Prevent duplicates

    selectedUsers.push({ id: userId, firstName, lastName });

    const selectedNames = document.getElementById("selected-names");
    selectedNames.innerHTML = selectedUsers
        .map(
            (user) =>
                `<span class="selected-user">
                    ${user.firstName} ${user.lastName} 
                    <span class="remove-user" onclick="removeUser(${user.id})">X</span>
                </span>`
        )
        .join("");

    const searchInput = document.getElementById("search-input");
    searchInput.value = ""; // Clear input after adding a user

    console.log("Selected users: ")
    for(let i = 0; i < selectedUsers.length; i++){
    console.log(selectedUsers[i].firstName)
    }
}

// Removes a user from the selected users list
function removeUser(userId) {
    // Ensure matching by type
    selectedUsers = selectedUsers.filter((user) => user.id !== String(userId));

    // Update the capsules
    const selectedNames = document.getElementById("selected-names");
    selectedNames.innerHTML = selectedUsers
        .map(
            (user) =>
                `<span class="selected-user">
                    ${user.firstName} ${user.lastName} 
                    <span class="remove-user" onclick="removeUser('${user.id}')">X</span>
                </span>`
        )
        .join("");
    console.log("Selected users: ")
    for(let i = 0; i < selectedUsers.length; i++){
        console.log(selectedUsers[i].firstName)
    }
}


// console.log("Selected users: ")
// for(let i = 0; i < selectedUsers.length; i++){
//     console.log(selectedUsers[i].firstName)
// }
