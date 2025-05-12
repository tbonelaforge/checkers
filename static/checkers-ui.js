/*
var moves = [{"type": "move", "current": [1, 4], "final": [0, 3]},{"type": "move", "current": [1, 4], "final": [0, 5]},{"type": "move", "current": [3, 6], "final": [2, 7]}];
*/
/*
var currentPlayer = 'r'; // Could also be 'b'
*/
let theseMoves = null;
let state = "nothing"; // Could also be 'showing_moves' or 'dragging', 


function handleTableClick(event) {
    var srcElement = event.srcElement;
    var i = srcElement.getAttribute('i');
    var j = srcElement.getAttribute('j');
}
function handleMouseDown(event) {
    if (state === 'showing_moves') {
        state = 'dragging';
        event.preventDefault();
    }
}

function handleMouseUp(event) {
    if (state === 'dragging') {
        var srcElement = event.srcElement;
        
        if (isActive(srcElement)) {
            clearMoves();
            showMoves(srcElement);
            state = 'showing_moves';
            return;    
        } else {
            const correspondingMove = findCorrespondingMove(srcElement);
            if (correspondingMove) {
                fetch("/move", {
                    method: 'POST',
                    body: JSON.stringify(correspondingMove),
                    headers: {
                        'Content-type': 'application/json'
                    }
                }).then(function(fetchResponse) {
                    window.location.reload();
                });
                
            } else {
                clearMoves();
                state = 'nothing';
            }
        }
    }
    

}

function getCoords(srcElement) {
    return [
        Number(srcElement.getAttribute('i')),
        Number(srcElement.getAttribute('j'))
    ];
}

function findCorrespondingMove(finalPositionSrcElement) {
    if (!theseMoves) {
        return null;
    }
    const [i, j] = getCoords(finalPositionSrcElement);
    return theseMoves.find(function(move) {
        return (move.final[0] === i && move.final[1] === j);
    });
}

function isActive(srcElement) {
    const [i, j] = getCoords(srcElement);
    if (!moveHash[i]) {
        return false;
    }
    if (!moveHash[i][j]) {
        return false;
    }
    return true;
}

function getMoveElements(theseMoves) {
    const moveElements = [];
    for (const move of theseMoves) {
        const moveId = `${move.final[0]}_${move.final[1]}`;
        const moveElement = document.getElementById(moveId);
        moveElements.push(moveElement);
    }
    return moveElements;
}

function showMoves(srcElement) {
    // assert this element is active
    const [i, j] = getCoords(srcElement);
    theseMoves = moveHash[i][j];

    for (const moveElement of getMoveElements(theseMoves)) {
        addClass(moveElement, 'highlighted');
    }

    // debugging element
    const temp = document.createElement('span');
    temp.setAttribute('id', 'temp');
    temp.textContent = theseMoves.map(m => JSON.stringify(m)).join(',');
    document.body.append(temp);
}

function clearMoves() {
    for (const moveElement of getMoveElements(theseMoves)) {
        removeClass(moveElement, 'highlighted');
    }
    theseMoves = null;

    // debugging display element
    const temp = document.getElementById('temp');
    document.body.removeChild(temp);
}

function addClass(e, classStr) {
    const classAttr = e.getAttribute('class');
    e.setAttribute('class', classAttr + ` ${classStr}`);
}

function removeClass(e, classStr) {
    const classAttr = e.getAttribute('class');
    const splitClassAttrs = classAttr.split(' ');
    const removed = splitClassAttrs.filter((c) => c !== classStr);
    e.setAttribute('class', removed.join(' '));
}

function handleMouseEnter(event) {
    const srcElement = event.srcElement;
    if (state === 'nothing') {
        if (isActive(srcElement)) {
            showMoves(srcElement);
            state = 'showing_moves';
            return;
        }
    }
    if (state === 'showing_moves') {
        if (isActive(srcElement)) {
            showMoves(srcElement);
            state = 'showing_moves';
            return;
        } else {
            clearMoves();
            state = 'nothing';
            return;
        }
    }
}

function processMoves(moves) {
    /*
        moves = [{"type": "move", "current": [1, 4], "final": [0, 3]},{"type": "move", "current": [1, 4], "final": [0, 5]},{"type": "move", "current": [3, 6], "final": [2, 7]}];
    */
    // Need: to know which positions have moves available, and for those, which new positions the move produces.
    const moveHash = {}
    for (const move of moves) {
        const i = move.current[0];
        const j = move.current[1];
        if (!moveHash[i]) {
            moveHash[i] = {};
        }
        if (!moveHash[i][j]) {
            moveHash[i][j] = [];
        }
        moveHash[i][j].push(move);
    }
    return moveHash;
}

const moveHash = processMoves(moves);

function isGameOver() {
    const winnerMessageElement = document.getElementById('winner-message');
    if (winnerMessageElement) {
        return true;
    }
    return false;
}

window.onload = function () {
    if (isGameOver()) {
        return;
    }
    if (currentPlayer == 'r') {
        setTimeout(function() {
            fetch("/move", {
                method: 'POST',
                body: JSON.stringify({"type": "computer_move"}),
                headers: {
                    'Content-type': 'application/json'
                }
            }).then(function(fetchResponse) {
                window.location.reload();
            });
        }, 1000);
    } else {
        var t = document.getElementById("checkers-board");
        t.onmousedown = handleMouseDown;
        t.onmouseup = handleMouseUp;
        const cells = document.getElementsByTagName('td');
        for (const cell of cells) {
            cell.onmouseenter = handleMouseEnter;
        }
    }
};
