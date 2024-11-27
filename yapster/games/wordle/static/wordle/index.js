import { WORDS } from "./wordlist.js";

const keyboard = document.querySelector(".keyboard");
const keys = document.querySelectorAll(".key");

document.addEventListener("keydown", handleKeyboardInput);
keyboard.addEventListener("click", handleOnScreenKeyboardInput);


let guessCount = 0;
let letterCount = 0;
let guess = "";

function handleKeyboardInput(e) {
	const key = e.key.toUpperCase();

	if (key == " ") {
		return;
	}
	if (key == "BACKSPACE") {
		eraseLetter();
		return;
	}
	if (key == "ENTER") {
		submitGuess();
		return;
	}

	if (isLetter(key)) setTileText(key);
}

function handleOnScreenKeyboardInput(e) {
	const target = e.target.getAttribute("data-key");
	if (!target) {
		return;
	}
	const key = target.toUpperCase();

	if (key == "BACKSPACE") {
		eraseLetter();
		return;
	}
	if (key == "ENTER") {
		submitGuess();
		return;
	}

	if (isLetter(key)) setTileText(key);
}

function eraseLetter() {
	if (letterCount == 0) {
		return;
	}
	getCurrTile().textContent = "";
	guess = guess.slice(0, -1);
	letterCount--;
}

function getCurrTile() {
	const currRow = document.getElementsByClassName("row")[guessCount];
	return currRow.getElementsByClassName("tile")[letterCount - 1];
}

function setTileText(letter) {
	if (letterCount == 5) {
		return;
	}
	const currRow = document.getElementsByClassName("row")[guessCount];
	const currTile = currRow.getElementsByClassName("tile")[letterCount];
	currTile.textContent = letter;
	guess += letter;
	letterCount++;
}

function isLetter(letter) {
	const letterASCIIValue = letter.charCodeAt(0);
	const capsLetter = letterASCIIValue >= 65 && letterASCIIValue <= 90;
	const smallLetter = letterASCIIValue >= 97 && letterASCIIValue <= 122;
	const length = letter.length === 1;
	return length && (capsLetter || smallLetter);
}

function checkCorrectLetter(guessLetter, wordLetter, SECRET_WORD) {
	if (guessLetter === wordLetter) return "correct";
	else if (SECRET_WORD.includes(guessLetter)) return "slightly-correct";
	else return "wrong";
}

function submitGuess() {
	if (letterCount != 5) {
		alert("not enough letters");
		return;
	}
	checkGuess();
}

function checkGuess() {
	guess = guess.toLowerCase();
	SECRET_WORD = SECRET_WORD.toLowerCase();

	if (!WORDS.includes(guess)) {
		console.log(guess);
		alert(`INVALID WORD`);
		return;
	}
	updateColors();

	if (guess == SECRET_WORD) {
		gameWin();
		return;
	}

	letterCount = 0;
	if (guessCount < 5) guessCount++;
	guess = "";
}

function gameWin() {
	guessCount++;
	alert(`YOU GUESSED THE WORD IN ${guessCount} TRIES!`);
	document.removeEventListener("keydown", handleKeyboardInput);
	keyboard.removeEventListener("click", handleOnScreenKeyboardInput);

	const chatRoom = window.localStorage.getItem('chatName')
	const boardCont = document.querySelector('.board-cont');
	boardCont.innerHTML += `
		<div class="win-cont">
			<h2 class="win-cont__title">Guessed in ${guessCount} tries!</h2>	
			<h2 class="win-cont__word">${SECRET_WORD}</h2>	
			<a href=/chat/${chatRoom} class="win-cont__button">Share</a>
		</div>
	`

	window.localStorage.setItem('guessCount', guessCount)

	console.log(`CHAT NAEEEEEEEEEEEEEEEEEEEEEE ${chatRoom}`)
}

function updateColors() {
  for (let i = 0; i < SECRET_WORD.length; i++) {
    const currRow = document.getElementsByClassName("row")[guessCount];
    const currLetter = currRow.getElementsByClassName("tile")[i];
    const guessL = guess[i];
    const wordL = SECRET_WORD[i];
    const correctness = checkCorrectLetter(guessL, wordL, SECRET_WORD);

    currLetter.classList.add(correctness);
    
    console.log(guessL);

    const keyboardKey = document.getElementById(guessL);
    console.log(keyboardKey);
    keyboardKey.classList.add(correctness);
  }
}

