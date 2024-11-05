const dots = document.querySelector("#dots");

dots.addEventListener("click", () => {
	const options = document.querySelector("#dots-options");
	options.classList.toggle("hidden");
});
