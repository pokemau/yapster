const dots = document.querySelector("#dots");
const options = document.querySelector("#dots-options");

dots.addEventListener("click", () => {
	options.classList.toggle("hidden");
});
