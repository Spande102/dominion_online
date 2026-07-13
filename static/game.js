const socket = io();
let myName = null;
let lastState = null;

// Interaction State
let interactionMode = false;
let interactionPayload = null;
let selectedIndices = new Set();
let selectedSupplyNames = new Set();
let pendingCardName = null; // Track what card initiated this? 
let lastPlayedCardName = null; // Store for re-submission
let isDarkMode = false;


// Check if already logged in logic can stay, or strict resetting for strict lobby
const savedName = localStorage.getItem('dominion_player_name');
if (savedName) {
    // Optional: Auto-rejoin functionality could go here, but for now let's force selection for logic clarity
    // selectSeat(savedName); 
}

function selectSeat(name) {
    myName = name;
    localStorage.setItem('dominion_player_name', myName);

    // UI Update
    document.getElementById('seat-selection').style.display = 'none';

    if (name === 'Player 1') {
        document.getElementById('host-settings').style.display = 'block';
    } else {
        document.getElementById('waiting-message').style.display = 'block';
        // Non-hosts just wait for game_start event or state update
    }
}

function toggleManualInput() {
    const mode = document.getElementById('kingdom-mode').value;
    document.getElementById('manual-input-area').style.display = mode === 'manual' ? 'block' : 'none';
    document.getElementById('random-options').style.display = mode === 'random' ? 'block' : 'none';
}

function startGame() {
    const numPlayers = document.getElementById('num-players').value;
    const kingdomMode = document.getElementById('kingdom-mode').value;

    // Gather expansions
    const expansions = Array.from(document.querySelectorAll('input[name="expansion"]:checked')).map(cb => cb.value);
    const includePlatCol = document.getElementById('include-plat-col').checked;

    // Gather manual cards
    const manualInput = document.getElementById('manual-card-list').value;
    const manualCards = manualInput ? manualInput.split(',').map(s => s.trim()).filter(s => s.length > 0) : [];

    socket.emit('setup_game', {
        num_players: numPlayers,
        kingdom_mode: kingdomMode,
        expansions: expansions,
        include_platinum_colony: includePlatCol,
        manual_kingdom_cards: manualCards
    });
}

socket.on('connect', () => {
    console.log("Connected to server");
});

socket.on('game_start', () => {
    document.getElementById('lobby-overlay').style.display = 'none';
    document.getElementById('game-container').style.display = 'grid';
    document.getElementById('my-identity').innerText = `You are: ${myName} `;
});

socket.on('game_state', (state) => {
    console.log("New State:", state);

    // If we receive state and overlay is still up (e.g. late joiner), hide overlay
    if (state && document.getElementById('lobby-overlay').style.display !== 'none') {
        document.getElementById('lobby-overlay').style.display = 'none';
        document.getElementById('game-container').style.display = 'grid';
        if (myName) document.getElementById('my-identity').innerText = `You are: ${myName} `;
    }

    // Safety check: if state says Game Over but we just reset...
    if (state.game_over && sessionStorage.getItem('just_reset') === 'true') {
        console.log("Ignoring Game Over state due to fresh reset flag.");
        return;
    }

    lastState = state;
    renderGame(state);
});

socket.on('log', (data) => {
    addLogEntry(data.message, 'game-log', 'log-content');
});

socket.on('chat_log', (data) => {
    addLogEntry(`${data.player}: ${data.message} `, 'chat-log', 'chat-content');
});

function addLogEntry(text, type, containerId = 'log-content') {
    const logs = document.getElementById(containerId);
    if (!logs) return;
    const lastEntry = logs.lastElementChild;

    // Aggregation Logic for Game Logs
    if (type === 'game-log' && lastEntry && lastEntry.dataset.rawText === text) {
        let count = parseInt(lastEntry.dataset.count || 1) + 1;
        lastEntry.dataset.count = count;
        lastEntry.innerText = `${text} (x${count})`;
    } else {
        const div = document.createElement('div');
        div.className = 'log-entry ' + type;
        div.innerText = text;
        div.dataset.rawText = text;
        div.dataset.count = 1;
        logs.appendChild(div);
    }
    logs.scrollTop = logs.scrollHeight;
}

socket.on('error', (data) => {
    alert(data.message);
});

socket.on('game_over_resignation', (data) => {
    alert(`Game Over: ${data.player_name} resigned.`);
    location.reload();
});

function renderGame(state) {
    if (!state) return;

    updateBackground(state);

    // Check Game Over
    if (state.game_over) {
        // Do not return early, allow rendering board state
        // showGameOver(state.final_scores); <-- Removed
        // Instead, we will show a "Return to Lobby" button in controls
        // Log has likely been updated by server with scores.
    }

    // Status Bar
    document.getElementById('current-player').innerText = `Turn: ${state.current_player} `;
    document.getElementById('phase').innerText = `Phase: ${state.phase.toUpperCase()} `;

    // Find my player data
    const myData = state.players.find(p => p.name === myName);

    if (myData) {
        document.getElementById('actions').innerText = myData.actions;
        document.getElementById('buys').innerText = myData.buys;
        document.getElementById('coins').innerText = myData.coins;
        document.getElementById('vp-tokens').innerText = myData.victory_tokens;

        // Render Hand
        // Pass null for onclick because renderCardList handles hand clicks specially now
        renderCardList('hand-cards', myData.hand, null);

        // Render My Discard
        const discardDiv = document.getElementById('discard-pile');
        if (myData.discard_pile.length > 0) {
            const topCard = myData.discard_pile[myData.discard_pile.length - 1];
            discardDiv.innerText = `${topCard} (${myData.discard_pile.length})`;
        } else {
            discardDiv.innerText = "Empty";
        }

    } else {
        document.getElementById('hand-cards').innerHTML = '<em>Spectating or invalid name...</em>';
    }

    // Render Supply
    const supplyKingdomDiv = document.getElementById('supply-kingdom');
    const supplyBaseDiv = document.getElementById('supply-base');
    supplyKingdomDiv.innerHTML = '';
    supplyBaseDiv.innerHTML = '';

    const baseCards = ["Copper", "Silver", "Gold", "drivers", "Estate", "Duchy", "Province", "Curse", "Platinum", "Colony"];

    for (const [name, count] of Object.entries(state.supply_counts)) {
        if (count > 0 || (state.supply[name] && count === 0)) { // Show empty piles too potentially, or just usually empty piles remain but count is 0
            const cost = state.supply[name];
            // Supply Click Handler
            let handler = () => buyCard(name);
            if (interactionMode && interactionPayload.type === 'select_from_supply') {
                handler = () => handleSupplyCardClick(name);
            }

            const el = createCardElement(`${name} (${cost})`, handler);

            // Selection Style for Supply
            if (interactionMode && selectedSupplyNames.has(name)) {
                el.classList.add('selected-card');
            }

            const badge = document.createElement('div');
            badge.innerText = count;
            badge.style.fontWeight = 'bold';
            el.appendChild(badge);

            if (baseCards.includes(name)) {
                supplyBaseDiv.appendChild(el);
            } else {
                supplyKingdomDiv.appendChild(el);
            }
        }
    }

    // Visibility of Play Treasures Button
    // Show only if phase is 'action' (and have treasures? logic complex) or 'buy'
    // Typically played in buy phase.
    const playTreasuresBtn = document.querySelector('button[onclick="playTreasures()"]');
    if (playTreasuresBtn) {
        if (state.phase === 'buy' && state.current_player === myName) {
            playTreasuresBtn.style.display = 'inline-block';
            playTreasuresBtn.style.display = 'none'; // Hide header button
        } else {
            playTreasuresBtn.style.display = 'none';
        }
    }

    // Add Play Treasures button to Play Area if Buy Phase OR Action Phase (convenience to skip actions)
    const actionsArea = document.getElementById('play-area');
    let existingBtn = document.getElementById('dynamic-play-treasures');
    // Allow playing treasures in Action phase (transitions to Buy) or obviously in Buy phase
    if ((state.phase === 'buy' || state.phase === 'action') && state.current_player === myName && !state.game_over) {
        if (!existingBtn) {
            const btn = document.createElement('button');
            btn.id = 'dynamic-play-treasures';
            btn.innerText = 'Play Treasures';
            btn.onclick = playTreasures;
            btn.style.marginLeft = '10px';
            document.querySelector('#play-area h2').appendChild(btn);
        }
    } else if (existingBtn) {
        existingBtn.remove();
    }

    // Game Over Button Logic
    const controlsDiv = document.getElementById('controls');
    if (state.game_over) {
        // Clear existing controls and show only Return to Lobby
        // We need to be careful not to create duplicates or flicker too much
        // But renderGame runs often.
        if (!controlsDiv.querySelector('#return-lobby-btn')) {
            // Create a container or just append? 
            // Ideally we might want to hide other buttons, but for now just appending is safe as long as we remove it later.
            // But user says it "stays". 

            // Let's hide the standard buttons if game is over to avoid clicking 'End Turn' in vain?
            // Actually, simplest fix for the "stays" bug is just to ensure it's removed if !game_over.

            controlsDiv.innerHTML = `<span id="my-identity" style="margin-right: 15px; font-weight: bold;">${document.getElementById('my-identity').innerText}</span>`;
            const btn = document.createElement('button');
            btn.id = 'return-lobby-btn';
            btn.innerText = 'Return to Lobby';
            btn.onclick = resetGame;
            btn.style.background = '#3498db';
            btn.style.color = 'white';
            controlsDiv.appendChild(btn);
        }
    } else {
        // Ensure Return to Lobby button is GONE if game is running
        const returnBtn = document.getElementById('return-lobby-btn');
        if (returnBtn) {
            // If we replaced innerHTML, we might need to restore original buttons?
            // Ah! creating the button REPLACED innerHTML above: 
            // controlsDiv.innerHTML = ...
            // So if we are in a new game, controlsDiv might be missing the original buttons if we don't reload!
            // But resetGame() calls reload(). 

            // Wait. If resetGame() calls reload(), the page resets to index.html state.
            // So controlsDiv comes back with "Play Treasures", "End Turn", "Resign".

            // So why does the button stay?
            // Maybe the user didn't click resetGame? 
            // Or maybe there's a race condition where game_over state is sent initially?

            // If game_over=false, we need to ensure standard controls are visible?
            // Since we don't have a templating engine client-side, restoring innerHTML is hard unless we save it.
            // BUT, since we expect a full reload on reset, this shouldn't be an issue unless the user is seeing a state update that adds the button *after* reload?

            // Let's just remove the button if it exists and we are not game over.
            // And if the standard buttons are missing (because we nuked them previously and didn't reload?), we are in trouble.
            // But we trust resetGame() reloads.

            returnBtn.remove();
        }
    }

    // Render In Play
    const currentPlayer = state.players[state.turn_index];
    renderCardList('in-play-cards', currentPlayer.in_play, null);

    // Render Trash
    const trashDiv = document.getElementById('trash-pile');
    if (state.trash.length > 0) {
        const topTrash = state.trash[state.trash.length - 1];
        trashDiv.innerText = `${topTrash} (${state.trash.length})`;
    } else {
        trashDiv.innerText = "Empty";
    }
}

function renderCardList(containerId, cards, onClick) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    const isHand = containerId === 'hand-cards';

    cards.forEach((cardName, index) => {
        // If in hand, we pass a special handler to support index-based selection
        let handler = null;
        if (isHand) {
            handler = () => handleHandCardClick(cardName, index);
        } else if (onClick) {
            handler = () => onClick(cardName);
        }

        const el = createCardElement(cardName, handler);

        if (!handler) el.style.cursor = 'default';

        // Apply selection style
        if (isHand && interactionMode && selectedIndices.has(index)) {
            el.classList.add('selected-card');
        }

        container.appendChild(el);
    });
}

function createCardElement(text, onClick) {
    const div = document.createElement('div');
    div.className = 'card';
    div.innerText = text;
    if (onClick) {
        div.onclick = onClick;
    }
    return div;
}

function playCard(cardName) {
    if (interactionMode) return; // Prevent playing other cards while selecting

    // Store this in case strictly needed, but typically we set it before emit
    lastPlayedCardName = cardName;
    socket.emit('play_card', { player_name: myName, card_name: cardName });
}

// let lastPlayedCardName = null; // Removed duplicate

// Interaction Handlers
socket.on('interaction_request', (payload) => {
    console.log("Interaction Requested:", payload);

    if (payload.player_name && payload.player_name !== myName) {
        // Optional: Visual indicator that someone else is thinking
        return;
    }

    interactionMode = true;
    interactionPayload = payload;
    selectedIndices.clear();
    selectedSupplyNames.clear();

    // UI
    document.getElementById('interaction-area').style.display = 'block';

    // Clear previous interaction helper content if any
    const container = document.getElementById('interaction-helper');
    container.innerHTML = '';

    // Check type
    if (payload.type === 'sentry_resolution') {
        document.getElementById('interaction-prompt').innerText = payload.prompt;
        renderSentryResolution(payload);
    } else {
        document.getElementById('interaction-prompt').innerText = payload.prompt;
        updateInteractionHelper();
        // Re-render hand to show selection mode (if we wanted specific visual cues)
        if (lastState) renderGame(lastState);
    }
});

// Sentry State
let sentryState = []; // [{ name: 'Copper', action: 'keep', id: 0 }, ...]

function renderSentryResolution(payload) {
    const container = document.getElementById('interaction-helper');
    container.innerHTML = ''; // Helper area is now our main custom area

    // Initialize state if first time (re-rendering might keep state?)
    // For now, reset state on new request
    sentryState = payload.cards.map((c, i) => ({ ...c, action: 'keep', originalIndex: i }));

    const wrapper = document.createElement('div');
    wrapper.id = 'sentry-wrapper';

    updateSentryUI(wrapper);
    container.appendChild(wrapper);

    // Hide standard buttons, show custom submit
    // Actually standard Confirm/Cancel might be visible.
    // Let's hide them or repurpose them. 
    // We'll hide the standard "Confirm" button and put our own "Done" inside the wrapper?
    // Or just hook `confirmInteraction`.
}

function updateSentryUI(container) {
    if (!container) container = document.getElementById('sentry-wrapper');
    if (!container) return;

    container.innerHTML = '';

    const cardsDiv = document.createElement('div');
    cardsDiv.className = 'sentry-cards';

    sentryState.forEach((item, index) => {
        const cardCol = document.createElement('div');
        cardCol.className = 'sentry-card-col';

        const cardEl = createCardElement(item.name);
        cardEl.style.cursor = 'default';
        if (item.action === 'trash') cardEl.classList.add('sentry-trash');
        if (item.action === 'discard') cardEl.classList.add('sentry-discard');

        cardCol.appendChild(cardEl);

        // Controls
        const controls = document.createElement('div');
        controls.className = 'sentry-controls';

        const trashBtn = document.createElement('button');
        trashBtn.innerText = 'Trash';
        trashBtn.className = item.action === 'trash' ? 'active' : '';
        trashBtn.onclick = () => {
            item.action = item.action === 'trash' ? 'keep' : 'trash';
            updateSentryUI();
        };

        const discardBtn = document.createElement('button');
        discardBtn.innerText = 'Discard';
        discardBtn.className = item.action === 'discard' ? 'active' : '';
        discardBtn.onclick = () => {
            item.action = item.action === 'discard' ? 'keep' : 'discard';
            updateSentryUI();
        };

        controls.appendChild(trashBtn);
        controls.appendChild(discardBtn);
        cardCol.appendChild(controls);

        cardsDiv.appendChild(cardCol);
    });

    container.appendChild(cardsDiv);

    // Reorder controls if multiple 'keep'
    const kept = sentryState.filter(i => i.action === 'keep');
    if (kept.length > 1) {
        const swapBtn = document.createElement('button');
        swapBtn.innerText = 'Swap Order';
        swapBtn.onclick = () => {
            // Swap indices in the 'kept' subset, then reflect in sentryState?
            // Actually sentryState order matters for top deck.
            // Let's just swap position of the two items in sentryState array.
            // If they are not adjacent in array, this is tricky. 
            // But usually only 2 cards.

            // Find indices of kept items in sentryState
            const idx1 = sentryState.indexOf(kept[0]);
            const idx2 = sentryState.indexOf(kept[1]);

            // Swap
            [sentryState[idx1], sentryState[idx2]] = [sentryState[idx2], sentryState[idx1]];
            updateSentryUI();
        };
        container.appendChild(swapBtn);

        const info = document.createElement('div');
        info.innerText = `Top: ${kept[0].name}, Second: ${kept[1].name}`;
        container.appendChild(info);
    } else if (kept.length === 1) {
        const info = document.createElement('div');
        info.innerText = `Top: ${kept[0].name}`;
        container.appendChild(info);
    } else {
        const info = document.createElement('div');
        info.innerText = `Deck will be empty.`;
        container.appendChild(info);
    }
}

function handleHandCardClick(cardName, index) {
    if (!interactionMode) {
        playCard(cardName);
    } else {
        if (interactionPayload && interactionPayload.type === 'sentry_resolution') return; // Hand disabled

        // Toggle selection
        if (selectedIndices.has(index)) {
            selectedIndices.delete(index);
        } else {
            selectedIndices.add(index);
        }
        updateInteractionHelper();
        // Re-render to show selection
        if (lastState) renderGame(lastState);
    }
}

function handleSupplyCardClick(cardName) {
    if (!interactionMode) return;
    if (interactionPayload && interactionPayload.type === 'sentry_resolution') return;

    // Toggle (Generic or Mixed)
    // Validate generic restrictions? Usually only 1 card from supply.
    // Let's assume max 1 for now unless specified generic.
    // In mixed mode or supply mode, we usually pick 1.

    if (selectedSupplyNames.has(cardName)) {
        selectedSupplyNames.delete(cardName);
    } else {
        selectedSupplyNames.clear(); // Single selection enforcement for now
        selectedSupplyNames.add(cardName);
    }
    updateInteractionHelper();
    if (lastState) renderGame(lastState);
}

function updateInteractionHelper() {
    if (interactionPayload && interactionPayload.type === 'sentry_resolution') return;

    const count = selectedIndices.size;
    const msg = `Selected: ${count} cards.`;
    document.getElementById('interaction-helper').innerText = msg;
}

function confirmInteraction() {
    if (!interactionMode) return;

    let finalSelection = [];

    if (interactionPayload && interactionPayload.type === 'sentry_resolution') {
        const trash = sentryState.filter(i => i.action === 'trash').map(i => i.name);
        const discard = sentryState.filter(i => i.action === 'discard').map(i => i.name);
        // Top deck: kept items in current order
        const top_deck = sentryState.filter(i => i.action === 'keep').map(i => i.name);

        finalSelection = { trash, discard, top_deck };
    } else if (interactionPayload && interactionPayload.type === 'select_from_supply') {
        finalSelection = Array.from(selectedSupplyNames);
    } else {
        // Convert indices to names
        const myData = lastState.players.find(p => p.name === myName);
        if (!myData) return;
        const selectedNames = [];
        selectedIndices.forEach(idx => {
            if (myData.hand[idx]) selectedNames.push(myData.hand[idx]);
        });
        finalSelection = selectedNames;
    }

    socket.emit('submit_interaction', {
        player_name: myName,
        selection: finalSelection
    });

    endInteraction();
}

function cancelInteraction() {
    if (interactionPayload && interactionPayload.type === 'sentry_resolution') {
        // Can we cancel? Sentry is mandatory once played? 
        // We can just submit empty/default. 
        // Or "Undo" play? No.
        // Let's just treat cancel as "submit current state" or alert "Must finish".
        alert("Please finish resolving Sentry.");
        return;
    }
    endInteraction();
}

function endInteraction() {
    interactionMode = false;
    interactionPayload = null;
    selectedIndices.clear();
    document.getElementById('interaction-area').style.display = 'none';
    const helper = document.getElementById('interaction-helper');
    if (helper) helper.innerHTML = ''; // Clean up sentry UI
    if (lastState) renderGame(lastState);
}

function buyCard(cardName) {
    socket.emit('buy_card', { player_name: myName, card_name: cardName });
}

function playTreasures() {
    socket.emit('play_treasures', { player_name: myName });
}

function endTurn() {
    socket.emit('end_turn', { player_name: myName });
}

function sendChat() {
    const input = document.getElementById('chat-input');
    const msg = input.value.trim();
    if (msg) {
        socket.emit('chat_message', { player_name: myName, message: msg });
        input.value = '';
    }
}

function resignGame() {
    if (confirm("Are you sure you want to resign? The game will end for everyone.")) {
        socket.emit('resign', { player_name: myName });
    }
}

// Chat enter key
document.getElementById('chat-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendChat();
    }
});

function toggleDarkMode() {
    isDarkMode = !isDarkMode;
    document.body.classList.toggle('dark-mode', isDarkMode);
    updateBackground(lastState); // Re-check background rules
}

// Background Logic
let useMonasteryArt = Math.random() < 0.5; // 50% chance on load
console.log("Using Monastery Art:", useMonasteryArt);

function updateBackground(state) {
    if (!state) return;

    const body = document.body;

    // Night Mode Logic
    if (state.phase.toLowerCase() === 'night' || state.phase.toLowerCase() === 'night phase') {
        body.classList.add('night-mode');
        // Specific user request: "In night phase, the screen should also feel sort of like night (so dark mode on etc.)"
        // And "monastaryart is the background of the game randomly" 
        // User said: "make the image in assets the background whenever it is a players night phase"
        // Wait, did they mean the image ONLY in night phase? 
        // "fix it so that the monastaryart is the background of the game randomly. In night phase, the screen should also feel sort of like night"
        // I interpolate: 
        // 1. Random Background choice (Monastery OR Default) is global.
        // 2. Night Phase turns on Dark Mode (filters).

        // OR:
        // "monastaryart is the background ... In night phase ... feel sort of like night"

        // Let's stick to the plan:
        // If useMonasteryArt is true, set background image.
        // If night phase, add .night-mode.
    } else {
        body.classList.remove('night-mode');
    }

    if (useMonasteryArt) {
        body.style.backgroundImage = "url('/static/MonasteryArt.png')";
        body.style.backgroundSize = "cover";
        body.style.backgroundPosition = "center";
        body.style.backgroundAttachment = "fixed";
    } else {
        body.style.backgroundImage = "";
    }
}

function showGameOver(scores) {
    const overlay = document.getElementById('game-over-overlay');
    const board = document.getElementById('score-board');
    if (!overlay || !board) return;

    // Sort scores
    // scores is object { "Player 1": 10, "Player 2": 15 }
    const sorted = Object.entries(scores || {}).sort((a, b) => b[1] - a[1]);

    let html = '<table style="width:100%; border-collapse:collapse;">';
    html += '<tr><th style="text-align:left; border-bottom:1px solid #ddd; padding:5px;">Player</th><th style="text-align:right; border-bottom:1px solid #ddd; padding:5px;">Points</th></tr>';

    sorted.forEach(([player, score]) => {
        const isWinner = score === sorted[0][1];
        const style = isWinner ? 'font-weight:bold; color:#27ae60;' : '';
        const trophy = isWinner ? ' 🏆' : '';
        html += `<tr><td style="padding:8px; border-bottom:1px solid #eee; ${style}">${player}${trophy}</td><td style="text-align:right; padding:8px; border-bottom:1px solid #eee; ${style}">${score}</td></tr>`;
    });
    html += '</table>';

    board.innerHTML = html;

    board.innerHTML = html;

    // Force display flex as defined in HTML style
    overlay.style.display = 'flex';
}

function resetGame() {
    window.location.href = '/reset';
}

socket.on('game_reset', () => {
    // Hide all game stuff, show lobby
    document.getElementById('game-over-overlay').style.display = 'none';
    document.getElementById('game-container').style.display = 'none';
    document.getElementById('lobby-overlay').style.display = 'flex'; // Assuming flex for centering lobby

    // Reset local state if needed
    lastState = null;
    sessionStorage.setItem('just_reset', 'true');
    location.reload(); // Simplest clean slate
});

