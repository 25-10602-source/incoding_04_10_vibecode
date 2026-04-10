const COLUMNS = 17;
const ROWS = 10;
const TIME_LIMIT = 120; // seconds

const board = document.getElementById('game-board');
const scoreEl = document.getElementById('score');
const timerEl = document.getElementById('timer');
const selectionBox = document.getElementById('selection-box');
const startScreen = document.getElementById('start-screen');
const startBtnOverlay = document.getElementById('start-btn-overlay');
const gameOverScreen = document.getElementById('game-over-screen');
const finalScoreEl = document.getElementById('final-score');
const restartBtn = document.getElementById('restart-btn');

let score = 0;
let timeLeft = TIME_LIMIT;
let timerInterval;
let isPlaying = false;

let isDragging = false;
let startX, startY;
let currentX, currentY;

let apples = [];

// Initialize board contents without starting timer yet
function prepareBoard() {
    board.innerHTML = '';
    apples = [];

    // Fill grid
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLUMNS; c++) {
            const appleWrapper = document.createElement('div');
            appleWrapper.style.width = '100%';
            appleWrapper.style.height = '100%';
            appleWrapper.style.display = 'flex';
            appleWrapper.style.justifyContent = 'center';
            appleWrapper.style.alignItems = 'flex-end'; // Align to bottom so stem doesn't overflow grid top boundary

            const apple = document.createElement('div');
            apple.classList.add('apple');
            
            const num = Math.floor(Math.random() * 9) + 1;
            apple.textContent = num;
            apple.dataset.val = num;
            
            const isBonus = Math.random() < 0.2;
            if (isBonus) {
                apple.classList.add('bonus');
            }
            
            appleWrapper.appendChild(apple);
            board.appendChild(appleWrapper);
            
            apples.push({
                element: apple,
                wrapper: appleWrapper,
                val: num,
                cleared: false,
                isBonus: isBonus
            });
        }
    }
    
    // We update bounds initially although the start screen obscures it
    setTimeout(updateAppleBounds, 50);
}

function initGame() {
    prepareBoard();
    
    score = 0;
    timeLeft = TIME_LIMIT;
    scoreEl.textContent = score;
    timerEl.textContent = timeLeft;
    
    // Hide screens
    startScreen.classList.add('hidden');
    gameOverScreen.classList.add('hidden');
    
    isPlaying = true;
    startTimer();
}

function updateAppleBounds() {
    const boardRect = board.getBoundingClientRect();
    apples.forEach(item => {
        const rect = item.wrapper.getBoundingClientRect();
        item.left = rect.left - boardRect.left;
        item.top = rect.top - boardRect.top;
        item.right = item.left + rect.width;
        item.bottom = item.top + rect.height;
    });
}

function startTimer() {
    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        timeLeft--;
        timerEl.textContent = timeLeft;
        if (timeLeft <= 0) {
            endGame();
        }
    }, 1000);
}

function endGame() {
    isPlaying = false;
    clearInterval(timerInterval);
    gameOverScreen.classList.remove('hidden');
    finalScoreEl.textContent = score;
    selectionBox.style.display = 'none';
}

startBtnOverlay.addEventListener('click', initGame);
restartBtn.addEventListener('click', initGame);

// Interaction Logic
function getPointerPos(e) {
    if (e.touches && e.touches.length > 0) {
        return { x: e.touches[0].clientX, y: e.touches[0].clientY };
    }
    return { x: e.clientX, y: e.clientY };
}

function handleStart(e) {
    if (!isPlaying) return;
    if (e.type === 'touchstart') e.preventDefault(); 
    
    isDragging = true;
    
    const boardRect = board.getBoundingClientRect();
    const pos = getPointerPos(e);
    
    startX = pos.x - boardRect.left;
    startY = pos.y - boardRect.top;
    
    startX = Math.max(0, Math.min(startX, boardRect.width));
    startY = Math.max(0, Math.min(startY, boardRect.height));
    
    selectionBox.style.display = 'block';
    selectionBox.style.left = startX + 'px';
    selectionBox.style.top = startY + 'px';
    selectionBox.style.width = '0px';
    selectionBox.style.height = '0px';

    highlightSelectedApples(startX, startY, 0, 0);
}

function handleMove(e) {
    if (!isDragging || !isPlaying) return;
    if (e.type === 'touchmove') e.preventDefault();
    
    const boardRect = board.getBoundingClientRect();
    const pos = getPointerPos(e);
    
    currentX = pos.x - boardRect.left;
    currentY = pos.y - boardRect.top;
    
    currentX = Math.max(0, Math.min(currentX, boardRect.width));
    currentY = Math.max(0, Math.min(currentY, boardRect.height));

    const left = Math.min(startX, currentX);
    const top = Math.min(startY, currentY);
    const width = Math.abs(currentX - startX);
    const height = Math.abs(currentY - startY);

    selectionBox.style.left = left + 'px';
    selectionBox.style.top = top + 'px';
    selectionBox.style.width = width + 'px';
    selectionBox.style.height = height + 'px';

    highlightSelectedApples(left, top, width, height);
}

function handleEnd(e) {
    if (!isDragging) return;
    isDragging = false;
    selectionBox.style.display = 'none';
    checkSelection();
}

board.addEventListener('mousedown', handleStart);
document.addEventListener('mousemove', handleMove);
document.addEventListener('mouseup', handleEnd);

board.addEventListener('touchstart', handleStart, {passive: false});
document.addEventListener('touchmove', handleMove, {passive: false});
document.addEventListener('touchend', handleEnd);
document.addEventListener('touchcancel', handleEnd);

window.addEventListener('resize', () => {
    if (isPlaying) {
        updateAppleBounds();
    }
});

function highlightSelectedApples(left, top, width, height) {
    const boxRect = {
        left: left,
        top: top,
        right: left + width,
        bottom: top + height
    };

    apples.forEach(item => {
        if (item.cleared) return;
        
        const intersect = !(
            boxRect.right < item.left ||
            boxRect.left > item.right ||
            boxRect.bottom < item.top ||
            boxRect.top > item.bottom
        );

        if (intersect) {
            item.element.classList.add('selected');
        } else {
            item.element.classList.remove('selected');
        }
    });
}

function checkSelection() {
    let sum = 0;
    const selectedItems = [];
    
    apples.forEach(item => {
        if (item.element.classList.contains('selected')) {
            sum += item.val;
            selectedItems.push(item);
            item.element.classList.remove('selected');
        }
    });

    if (sum === 10) {
        selectedItems.forEach(item => {
            if (item.isBonus) {
                score += 5; // 보너스 사과는 5점
            } else {
                score += 1; // 일반 사과는 1점
            }
        });
        scoreEl.textContent = score;
        
        selectedItems.forEach(item => {
            item.cleared = true;
            item.element.classList.add('cleared');
            
            // 300ms 후 빈자리를 새로운 사과로 채움
            setTimeout(() => {
                const num = Math.floor(Math.random() * 9) + 1;
                item.val = num;
                item.element.textContent = num;
                item.element.dataset.val = num;
                
                item.isBonus = Math.random() < 0.2;
                if (item.isBonus) {
                    item.element.classList.add('bonus');
                } else {
                    item.element.classList.remove('bonus');
                }
                
                item.cleared = false;
                item.element.classList.remove('cleared');
            }, 300);
        });
    }
}

// Generate an initial board pattern immediately for background visuals on start screen
prepareBoard();
