const keys = document.querySelectorAll('.key');

// let input = [];
let guessCount = 0;
let letterCount = 0;

const getKeyPress = (e) => {
  const key = e.key;

  if (isBackspace(key)) {
    // erase letter
    eraseLetter();
    return;
  }

  setTileText(key)
  letterCount++;
  if (letterCount >= 5) {
    letterCount = 0;
    guessCount++;
  }
  if (guessCount > 5)
    guessCount = 0;
}

document.addEventListener('keydown', getKeyPress);

function eraseLetter() {
  getCurrTile().textContent = '';
  if (letterCount)
    letterCount--;
}

function getCurrTile() {
  const currRow = document.getElementsByClassName('row')[guessCount];
  return currRow.getElementsByClassName('tile')[letterCount];
}


function setTileText(letter) {
  const currRow = document.getElementsByClassName('row')[guessCount];
  const currTile = currRow.getElementsByClassName('tile')[letterCount];
  currTile.textContent = letter
}

function isBackspace(key) {
  return key == 'Backspace';
}