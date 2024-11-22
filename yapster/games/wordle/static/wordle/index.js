import { WORDS } from "./wordlist.js";

const keys = document.querySelectorAll('.key');

let guessCount = 0;
let letterCount = 0;
let guess = '';

function getKeyPress(e) {
  const key = e.key.toUpperCase();

  if (key == ' ') { return; }
  if (key == 'BACKSPACE') {
    eraseLetter();
    return;
  }
  if (key == 'ENTER') {
    submitGuess();
    return;
  } 


  if (isLetter(key)) 
    setTileText(key);
  console.log(letterCount)
}

document.addEventListener('keydown', getKeyPress);

function handleOnScreenKeyboardPress(e) {
  const target = e.target;
  const key= target.getAttribute('data-key');
  if (!key) { return; }
  if (key == 'backspace') {
    eraseLetter();
    return;
  }
  if (key == 'enter') {
    submitGuess();
    return;
  }

  if (isLetter(key))
    setTileText(key);
}

const keyboard = document.querySelector('.keyboard');
keyboard.addEventListener('click', handleOnScreenKeyboardPress);

function submitGuess() {
  if (letterCount != 5) {
    alert('not enough letters')
    return;
  }
  checkGuess();
  letterCount = 0;
  if (guessCount < 5)
    guessCount++;

  guess = '';
  // check if enough letters
  // check if last chance to guess
}

function checkGuess() {
  console.log(guess);
}

function eraseLetter() {
  if (letterCount == 0) { return; }
  getCurrTile().textContent = '';
  guess = guess.slice(0,-1);
  letterCount--;
}

function getCurrTile() {
  const currRow = document.getElementsByClassName('row')[guessCount];
  return currRow.getElementsByClassName('tile')[letterCount-1];
}

function setTileText(letter) {
  if (letterCount == 5) { return; }
  const currRow = document.getElementsByClassName('row')[guessCount];
  const currTile = currRow.getElementsByClassName('tile')[letterCount];
  currTile.textContent = letter;
  guess+=letter;
  letterCount++;
}

function isLetter(letter) {
  const letterASCIIValue = letter.charCodeAt(0);
  const capsLetter = letterASCIIValue >= 65 && letterASCIIValue <= 90;
  const smallLetter = letterASCIIValue >= 97 && letterASCIIValue <= 122;
  const length = letter.length === 1;
  return length && (capsLetter || smallLetter);
}