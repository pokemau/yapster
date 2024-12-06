import { WORDS } from "./wordlist.js";

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
const keyboard = document.querySelector(".keyboard");
const keys = document.querySelectorAll(".key");

document.addEventListener("keydown", handleKeyboardInput);
keyboard.addEventListener("click", handleOnScreenKeyboardInput);


let guessCount = 0;
let letterCount = 0;
let guess = "";
let guesses = [];


if (GAME.solved == 'True') {
	guesses = GAME.guesses
	fillBoard()
}

function fillBoard() {
	for (let i = 0; i < guesses.length; i++) {
		const word = guesses[i];
		guess = word
		for (let j = 0; j < word.length; j++) {
			setTileText(word[j])
		}
		updateColors()
		letterCount = 0
		guessCount++
	}

	const chatRoom = window.localStorage.getItem('chatName')
	const boardCont = document.querySelector('.board-cont');
	pauseEvents();

	boardCont.innerHTML += `
		<div class="win-cont">
			<h2 class="win-cont__title">Guessed in ${guessCount} ${guessCount === 1 ? 'try' : 'tries'}!</h2>	
			<h2 class="win-cont__word">${SECRET_WORD}</h2>	

			<div class="win-cont__btn-cont">
				<button class='win-cont__button ok-btn'>Ok</button>
			</div>
		</div>
	`
	
	document.querySelector('.ok-btn').addEventListener('click', () => {
		document.querySelector('.win-cont').classList.add('hidden')
	})

}


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
	if (letterCount == 5 && GAME.solved == 'False') {
		return;
	}
	const currRow = document.getElementsByClassName("row")[guessCount];
	const currTile = currRow.getElementsByClassName("tile")[letterCount];
	currTile.textContent = letter.toUpperCase();
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
		showMessage('MUST BE 5 LETTERS')
		return;
	}
	checkGuess();
}

function checkGuess() {
	guess = guess.toLowerCase();
	SECRET_WORD = SECRET_WORD.toLowerCase();

	if (!WORDS.includes(guess)) {
		showMessage('INVALID WORD')
		return;
	}
	
	guesses.push(guess)
	updateColors();

	if (guess == SECRET_WORD) {
		gameWin();
		return;
	}

	letterCount = 0;
	if (guessCount < 5) guessCount++;
	guess = "";
}

async function gameWin() {

	const chatRoom = window.localStorage.getItem('chatName')
	const boardCont = document.querySelector('.board-cont');

	await updateWordleGame(chatRoom);

	guessCount++;
	pauseEvents();

	boardCont.innerHTML += `
		<div class="win-cont">
			<h2 class="win-cont__title">Guessed in ${guessCount} ${guessCount === 1 ? 'try' : 'tries'}!</h2>	
			<h2 class="win-cont__word">${SECRET_WORD}</h2>	
			<a href=/chat/${chatRoom} class="win-cont__button">Share</a>
		</div>
	`
	window.localStorage.setItem('guessCount', guessCount)
}

async function updateWordleGame(chatRoom) {
	try {
		const gameID = window.location.href.split('/').pop()
		const response = await fetch(`/games/wordle/update_game/${gameID}`, {
			method: 'POST',
			headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
			},
			body: JSON.stringify({
				guesses: guesses.toString(),
			})
		})
		const data = await response.json()
		if (data.success) {
			console.log("UPDATED SUCCESSFULLY");
		} else {
			console.log(data.error);
		}
		
	} catch (error) {
		console.error(error)
	}
}

function pauseEvents() {
	document.removeEventListener("keydown", handleKeyboardInput);
	keyboard.removeEventListener("click", handleOnScreenKeyboardInput);
}
function resumeEvents() {
document.addEventListener("keydown", handleKeyboardInput);
keyboard.addEventListener("click", handleOnScreenKeyboardInput);
}

const messageCont = document.querySelector('.message-cont')
const messageP = document.querySelector('.message__content')
function showMessage(message) {
	document.querySelector('.message-cont').classList.remove('hidden')
	messageP.textContent = message;
	pauseEvents();
	setTimeout(() => {
		document.querySelector('.message-cont').classList.add('hidden')
		messageP.textContent = ''
		resumeEvents();
	}, 1000);
}

function updateColors() {
  for (let i = 0; i < SECRET_WORD.length; i++) {
    const currRow = document.getElementsByClassName("row")[guessCount];
    const currLetter = currRow.getElementsByClassName("tile")[i];
    const guessL = guess[i];
    const wordL = SECRET_WORD[i];
    const correctness = checkCorrectLetter(guessL, wordL, SECRET_WORD);
    currLetter.classList.add(correctness);
    const keyboardKey = document.getElementById(guessL);
    keyboardKey.classList.add(correctness);
  }
}

