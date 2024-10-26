const dots = document.querySelector("#dots");
const closeUserDetail = document.querySelector("#close-icon");

window.addEventListener("click", function (e) {
	e.preventDefault();
	console.log(e.target);
});

closeUserDetail.addEventListener("click", () => {
	document.querySelector("#right-sidebar").style.display = "none";
});

dots.addEventListener("click", () => {
	const options = document.querySelector("#dots-options");

	options.classList.toggle("hidden");
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

		if (data.success) {
			document.querySelector("#right-sidebar p").textContent = data.first_name;
			document.querySelector(
				"#right-username p"
			).textContent = `@${data.username}`;
			document.querySelector("#right-bio p").textContent =
				data.bio || "No bio available";
			document.querySelector("#right-sidebar").style.display = "block";
		}
	} catch (error) {
		console.error(error);
	}
}
