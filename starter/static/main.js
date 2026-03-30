// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let timerInterval = null;
let elapsedSeconds = 0;
let hintsUsed = 0;
let currentDifficulty = 'medium';
let solutionChecker = null;

// Dark Mode Management
function initializeDarkMode() {
  const darkModeToggle = document.getElementById('dark-mode-toggle');
  const isDarkMode = localStorage.getItem('darkMode') === 'true';
  
  // Set initial dark mode state
  if (isDarkMode) {
    document.body.classList.add('dark-mode');
  }
  
  // Add click event listener to toggle
  darkModeToggle.addEventListener('click', toggleDarkMode);
}

function toggleDarkMode() {
  const body = document.body;
  body.classList.toggle('dark-mode');
  const isDarkMode = body.classList.contains('dark-mode');
  localStorage.setItem('darkMode', isDarkMode);
}

// Local storage management for top scores
function getScores() {
  const scores = localStorage.getItem('sudoku_scores');
  return scores ? JSON.parse(scores) : [];
}

function saveScores(scores) {
  localStorage.setItem('sudoku_scores', JSON.stringify(scores));
}

function addScore(name, time, hints, difficulty) {
  const scores = getScores();
  scores.push({ name, time, hints, difficulty });
  // Sort by time (ascending) and keep only top 10
  scores.sort((a, b) => a.time - b.time);
  scores.splice(10);
  saveScores(scores);
  displayTopScores();
}

function displayTopScores() {
  const scores = getScores();
  const tbody = document.getElementById('scores-tbody');
  
  if (scores.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5">No scores yet</td></tr>';
    return;
  }
  
  tbody.innerHTML = '';
  scores.forEach((score, index) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${score.name}</td>
      <td>${formatTime(score.time)}</td>
      <td>${score.hints}</td>
      <td>${score.difficulty}</td>
    `;
    tbody.appendChild(row);
  });
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

async function validateCellInput(inputElement, row, col, value) {
  // Remove any previous validation classes
  inputElement.classList.remove('incorrect', 'valid-entry');
  
  if (value === '') {
    return; // Empty cell, no validation needed
  }
  
  const res = await fetch('/validate-cell', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({row, col, value: parseInt(value, 10)})
  });
  
  const data = await res.json();
  if (data.error) {
    return;
  }
  
  if (data.is_correct) {
    inputElement.classList.add('valid-entry');
  } else {
    inputElement.classList.add('incorrect');
  }
}

// Solution checker using event delegation
class SolutionChecker {
  constructor(boardElement) {
    this.boardElement = boardElement;
    this.solvedCells = new Set();
    
    // Attach delegated event listener to the board instead of individual cells
    this.boardElement.addEventListener('change', (e) => this.handleCellChange(e));
    this.boardElement.addEventListener('input', (e) => this.handleCellInput(e));
  }
  
  handleCellChange(e) {
    if (e.target.classList.contains('sudoku-cell') && !e.target.disabled) {
      const row = parseInt(e.target.dataset.row);
      const col = parseInt(e.target.dataset.col);
      const value = e.target.value;
      
      if (value === '') {
        this.solvedCells.delete(`${row}-${col}`);
      } else {
        this.solvedCells.add(`${row}-${col}`);
      }
      
      this.checkIfPuzzleComplete();
    }
  }
  
  handleCellInput(e) {
    if (e.target.classList.contains('sudoku-cell') && !e.target.disabled) {
      const row = parseInt(e.target.dataset.row);
      const col = parseInt(e.target.dataset.col);
      const value = e.target.value;
      
      // Clean input to only allow 1-9
      const cleanedValue = value.replace(/[^1-9]/g, '');
      e.target.value = cleanedValue;
      
      if (cleanedValue !== '') {
        validateCellInput(e.target, row, col, cleanedValue);
      } else {
        e.target.classList.remove('incorrect', 'valid-entry');
      }
    }
  }
  
  checkIfPuzzleComplete() {
    // Count non-disabled cells (user-filled cells)
    const allInputs = this.boardElement.querySelectorAll('.sudoku-cell:not(:disabled)');
    const filledCells = this.boardElement.querySelectorAll('.sudoku-cell:not(:disabled)');
    
    let emptyCount = 0;
    filledCells.forEach(cell => {
      if (cell.value === '') {
        emptyCount++;
      }
    });
    
    // If all cells are filled, prompt the user to check their solution
    if (emptyCount === 0) {
      const msg = document.getElementById('message');
      msg.style.color = '#ff9800';
      msg.innerText = 'All cells filled! Click "Check Solution" to verify.';
    }
  }
  
  getBoardState() {
    const board = [];
    for (let i = 0; i < SIZE; i++) {
      board[i] = [];
      for (let j = 0; j < SIZE; j++) {
        const input = this.boardElement.querySelector(
          `input[data-row="${i}"][data-col="${j}"]`
        );
        board[i][j] = input.value ? parseInt(input.value, 10) : 0;
      }
    }
    return board;
  }
}

function updateTimer() {
  elapsedSeconds++;
  document.getElementById('timer').innerText = formatTime(elapsedSeconds);
}

function startTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
  }
  elapsedSeconds = 0;
  document.getElementById('timer').innerText = '00:00';
  timerInterval = setInterval(updateTimer, 1000);
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function updateHintsDisplay() {
  document.getElementById('hints-counter').innerText = `Hints: ${hintsUsed}`;
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      // Add color class based on 3x3 box
      const boxRow = Math.floor(i / 3);
      const boxCol = Math.floor(j / 3);
      const boxIndex = boxRow * 3 + boxCol;
      input.classList.add(`box-${boxIndex}`);
      // Event listeners are now handled by event delegation in SolutionChecker
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  
  // Initialize the solution checker with event delegation
  const boardDiv = document.getElementById('sudoku-board');
  solutionChecker = new SolutionChecker(boardDiv);
  
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.classList.add('prefilled');
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

async function newGame() {
  const difficulty = document.getElementById('difficulty').value;
  currentDifficulty = difficulty;
  const res = await fetch(`/new?difficulty=${difficulty}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  document.getElementById('message').innerText = '';
  hintsUsed = 0;
  updateHintsDisplay();
  startTimer();
}

async function checkSolution() {
  if (!solutionChecker) {
    return;
  }
  
  const board = solutionChecker.getBoardState();
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.classList.remove('incorrect', 'valid-entry');
    if (incorrect.has(idx)) {
      inp.classList.add('incorrect');
    }
  }
  if (incorrect.size === 0) {
    stopTimer();
    msg.style.color = '#388e3c';
    msg.innerText = `Congratulations! You solved it in ${formatTime(elapsedSeconds)}! Hints used: ${hintsUsed}`;
    // Show name modal
    showNameModal();
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

async function getHint() {
  if (!solutionChecker) {
    return;
  }
  
  const board = solutionChecker.getBoardState();
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  // Fill in the hint value
  const row = data.row;
  const col = data.col;
  const boardDiv = document.getElementById('sudoku-board');
  const hintInput = boardDiv.querySelector(
    `input[data-row="${row}"][data-col="${col}"]`
  );
  hintInput.value = data.value;
  hintInput.classList.remove('incorrect', 'valid-entry');
  hintInput.classList.add('hinted');
  hintInput.disabled = true;
  hintsUsed++;
  updateHintsDisplay();
  msg.style.color = '#f57c00';
  msg.innerText = 'Hint provided!';
}

// Wire buttons
window.addEventListener('load', () => {
  initializeDarkMode();
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('get-hint').addEventListener('click', getHint);
  document.getElementById('submit-score').addEventListener('click', submitScore);
  // Display initial scores
  displayTopScores();
  // initialize
  newGame();
});

function showNameModal() {
  const modal = document.getElementById('name-modal');
  document.getElementById('modal-time').innerText = formatTime(elapsedSeconds);
  document.getElementById('modal-hints').innerText = hintsUsed;
  document.getElementById('modal-difficulty').innerText = currentDifficulty;
  document.getElementById('player-name').value = '';
  modal.style.display = 'block';
  document.getElementById('player-name').focus();
}

function submitScore() {
  const name = document.getElementById('player-name').value.trim();
  if (!name) {
    alert('Please enter your name');
    return;
  }
  addScore(name, elapsedSeconds, hintsUsed, currentDifficulty);
  document.getElementById('name-modal').style.display = 'none';
}