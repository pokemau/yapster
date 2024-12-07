let isCreateChatState = false; // Tracks the state of the search bar
let isAddMemberState = false; // Tracks the state for Add Member
let selectedUsers = []; // Stores selected users in create-chat state


function toggleCreateChatState() {
    if (isAddMemberState) toggleAddMemberState(); // Exit Add Member state if active
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
        resetSearchState(); // Use shared reset for consistency
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

// Recycle Create GC button for Add Member functionality
function toggleAddMemberState() {
    isCreateChatState = !isCreateChatState;
    
    // Update UI based on the state
    const selectedNames = document.getElementById("selected-names");
    const searchInput = document.getElementById("search-input");
    const exitButton = document.getElementById("exit-create-chat"); // Exit button
    const chatList = document.getElementById("chat-list"); // Existing chats
    const searchResults = document.getElementById("search-results"); // Queried users
    const currentChats = document.getElementById("current-chats"); // Current user's chats
    const addMemberButton = document.querySelector(".chat-create"); // Add Member button

    if (isCreateChatState) {
        selectedNames.style.display = "flex"; // Show selected names container
        searchInput.placeholder = "Add users to group...";
        searchInput.value = ""; // Clear input for new search
        if (exitButton) exitButton.style.display = "inline"; // Show exit button
        if (chatList) chatList.style.display = "none"; // Hide existing chats
        if (searchResults) searchResults.innerHTML = ""; // Clear search results
        if (currentChats) currentChats.style.display = "none"; // Hide current chats

        // Change button functionality to add members to group
        addMemberButton.textContent = "Add Member(s)";
        addMemberButton.onclick = addMemberToGroup;
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

        // Restore button functionality to toggle Add Member state
        addMemberButton.textContent = "Add a Member";
        addMemberButton.onclick = toggleAddMemberState;
    }
}

// Add selected users to the group chat
function addMemberToGroup() {
    // Extract user IDs from selectedUsers
    const userIds = selectedUsers.map(user => user.id);

    // Get the chat ID and current members
    const chatId = currentChatID; // Use your global currentChatID variable
    const currentMembers = chat_users_id; // List of current members in the chat (user IDs)

    // Check if at least one user is selected
    if (selectedUsers.length === 0) {
        alert("Please add at least one user.");
        return;
    }

    // Check for duplicates (if the user is already in the chat)
    for (const userId of userIds) {
        if (currentMembers.includes(userId)) {
            alert("This user is already a member of the group chat.");
            return;
        }
    }

    // Send the request to add members
    fetch(`/chat/${chatId}/add_members/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ user_ids: userIds, chat_id: chatId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // alert("Members added successfully!");
            // Update UI or reload chat to reflect changes
            location.reload()
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error("Error adding members:", error));
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

    console.log("Selected users:", selectedUsers);
}

// Removes a user from the selected users list
function removeUser(userId) {
    selectedUsers = selectedUsers.filter((user) => user.id !== String(userId));

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
    console.log("Selected users:", selectedUsers);
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
        if (!isCreateChatState && !isAddMemberState && currentChats) currentChats.style.display = "block"; // Show current chats
    }

    if (isCreateChatState || isAddMemberState) {
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
                throw new Error(`Failed to fetch users and chats: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (searchResults) {
                searchResults.style.display = "block";

                const userResults = data.users.map((user) => {
                    return `
                        <div class="user" onclick="addUser('${user.id}', '${user.first_name}', '${user.last_name}')">
                            <div class="left-profile-pic"></div>
                            <div class="name-time-msg">
                                <p class="name">${user.first_name} ${user.last_name}</p>
                                <p class="time-sent">@${user.username}</p>
                            </div>
                        </div>
                    `;
                });

                searchResults.innerHTML = userResults.join("");
                if (chatList) chatList.style.display = "none"; // Hide chats during search
            }
        })
        .catch((error) => console.error("Error fetching users and chats:", error));
}

// NEW: Reset shared search state
function resetSearchState() {
    const selectedNames = document.getElementById("selected-names");
    const searchInput = document.getElementById("search-input");
    const exitButton = document.getElementById("exit-create-chat");
    const chatList = document.getElementById("chat-list");
    const searchResults = document.getElementById("search-results");
    const currentChats = document.getElementById("current-chats");
    const createChatButton = document.querySelector(".chat-create");

    selectedNames.style.display = "none";
    selectedUsers = [];
    selectedNames.innerHTML = "";
    searchInput.placeholder = "Search chats or users...";
    searchInput.value = "";
    if (exitButton) exitButton.style.display = "none";
    if (chatList) chatList.style.display = "block";
    if (searchResults) searchResults.innerHTML = "";
    if (currentChats) currentChats.style.display = "block";
    if (createChatButton) createChatButton.style.display = "inline";

    isAddMemberState = false;
    isCreateChatState = false;
}