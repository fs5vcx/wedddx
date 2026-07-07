const API_BASE = '/api';

const gameState = {
    token: localStorage.getItem('miner_token') || '',
    user: null, currentMine: null,
    layers: [], miners: {},
    elevator: null, elevatorWorker: null, groundWorker: null,
    unlockedMines: [], nextLayer: null,
    goldPerSecond: 0, gems: 0, cash: 0,
    isGameRunning: false, lastSyncTime: 0,
    currentPanel: 'miners', selectedLayerId: null,
    musicEnabled: true, soundEnabled: true,
    oreColors: [
        { main: '#FFD700', dark: '#FFA000', light: '#FFECB3' },
        { main: '#FF8A65', dark: '#E64A19', light: '#FFCCBC' },
        { main: '#E0E0E0', dark: '#9E9E9E', light: '#F5F5F5' },
        { main: '#64B5F6', dark: '#1976D2', light: '#BBDEFB' },
        { main: '#EF5350', dark: '#C62828', light: '#FFCDD2' }
    ]
};

function api(endpoint, method = 'GET', data = null) {
    const headers = { 'Content-Type': 'application/json' };
    if (gameState.token) headers['Authorization'] = `Bearer ${gameState.token}`;
    return fetch(`${API_BASE}${endpoint}`, {
        method, headers, body: data ? JSON.stringify(data) : null
    }).then(res => res.json()).catch(() => ({ status: 'error', message: '网络错误' }));
}

function showToast(msg) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 2500);
}

function formatNumber(num) {
    if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T';
    if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
    if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
    if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K';
    return Math.floor(num).toString();
}

function calculateCost(base, level) {
    return Math.floor(base * Math.pow(1.5, level - 1));
}

function getOreColor(depth) {
    return gameState.oreColors[(depth - 1) % gameState.oreColors.length];
}

function createMinerHTML(helmetColor = '#FFD700', bodyColor = '#4169E1') {
    return `
        <div class="layer-miner">
            <div class="lm-helmet" style="background: linear-gradient(180deg, ${helmetColor}, ${adjustColor(helmetColor, -30)}); border-color: ${adjustColor(helmetColor, -50)};"></div>
            <div class="lm-face"></div>
            <div class="lm-body" style="background: linear-gradient(180deg, ${bodyColor}, ${adjustColor(bodyColor, -30)}); border-color: ${adjustColor(bodyColor, -50)};"></div>
            <div class="lm-pickaxe"></div>
        </div>
    `;
}

function createOreHTML(depth) {
    const color = getOreColor(depth);
    return `
        <div class="layer-ore">
            <div class="ore-piece" style="background: linear-gradient(135deg, ${color.main}, ${color.dark});"></div>
        </div>
    `;
}

function adjustColor(hex, amount) {
    const num = parseInt(hex.replace('#', ''), 16);
    const r = Math.max(0, Math.min(255, (num >> 16) + amount));
    const g = Math.max(0, Math.min(255, ((num >> 8) & 0x00FF) + amount));
    const b = Math.max(0, Math.min(255, (num & 0x0000FF) + amount));
    return '#' + (0x1000000 + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

function initGameUI() {
}

function createMiningEffect(x, y) {
    const layer = document.getElementById('effect-layer');
    
    const effect = document.createElement('div');
    effect.className = 'mining-effect';
    effect.textContent = '⚒️';
    effect.style.left = (x - 15) + 'px';
    effect.style.top = (y - 15) + 'px';
    layer.appendChild(effect);
    
    setTimeout(() => {
        effect.remove();
    }, 700);
    
    for (let i = 0; i < 3; i++) {
        setTimeout(() => {
            const gold = document.createElement('div');
            gold.className = 'gold-float';
            gold.textContent = '💰';
            gold.style.left = (x + (Math.random() - 0.5) * 30) + 'px';
            gold.style.top = (y + (Math.random() - 0.5) * 20) + 'px';
            gold.style.animationDelay = (i * 0.1) + 's';
            layer.appendChild(gold);
            setTimeout(() => gold.remove(), 1000);
        }, i * 100);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    initGameUI();
    initAuth();
    if (gameState.token) checkTokenAndLoadGame();
});

function initAuth() {
    const loginTab = document.querySelector('.tab-btn[data-tab="login"]');
    const registerTab = document.querySelector('.tab-btn[data-tab="register"]');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    
    loginTab.addEventListener('click', () => {
        loginTab.classList.add('active'); registerTab.classList.remove('active');
        loginForm.style.display = 'flex'; registerForm.style.display = 'none';
    });
    registerTab.addEventListener('click', () => {
        registerTab.classList.add('active'); loginTab.classList.remove('active');
        registerForm.style.display = 'flex'; loginForm.style.display = 'none';
    });
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        login(document.getElementById('login-username').value, document.getElementById('login-password').value);
    });
    registerForm.addEventListener('submit', (e) => {
        e.preventDefault();
        register(document.getElementById('reg-username').value, document.getElementById('reg-password').value);
    });
}

async function register(username, password) {
    const result = await api('/register', 'POST', { username, password });
    if (result.status === 'success') {
        gameState.token = result.token;
        localStorage.setItem('miner_token', result.token);
        showToast('注册成功！');
        loadGame();
    } else showToast(result.message || '注册失败');
}

async function login(username, password) {
    const result = await api('/login', 'POST', { username, password });
    if (result.status === 'success') {
        gameState.token = result.token;
        localStorage.setItem('miner_token', result.token);
        showToast('登录成功！');
        loadGame();
    } else showToast(result.message || '登录失败');
}

async function checkTokenAndLoadGame() {
    const result = await api('/game/status', 'GET');
    if (result.status === 'success') loadGame();
    else { gameState.token = ''; localStorage.removeItem('miner_token'); }
}

async function loadGame() {
    const result = await api('/game/status', 'GET');
    if (result.status !== 'success') { showToast('加载失败'); return; }
    
    const data = result.data;
    gameState.user = data.user;
    gameState.currentMine = data.current_mine;
    gameState.layers = data.layers;
    gameState.miners = {};
    data.miners.forEach(m => gameState.miners[m.layer_id] = m);
    gameState.elevator = data.elevator;
    gameState.elevatorWorker = data.elevator_worker;
    gameState.groundWorker = data.ground_worker;
    gameState.unlockedMines = data.unlocked_mines;
    gameState.nextLayer = data.next_layer;
    gameState.goldPerSecond = data.gold_per_second;
    gameState.gems = data.user.gems || 0;
    gameState.cash = data.user.cash || 0;
    
    const firstUnlocked = gameState.layers.find(l => l.unlocked);
    if (firstUnlocked) gameState.selectedLayerId = firstUnlocked.id;
    
    document.getElementById('auth-screen').classList.add('hidden');
    document.getElementById('game-screen').classList.remove('hidden');
    
    renderGame();
    startGameLoop();
    bindGameEvents();
    startElevatorAnimation();
    startMiningEffects();
    
    if (gameState.musicEnabled) {
        document.getElementById('bg-music').play().catch(() => {});
    }
    
    if (data.offline_earned > 0) {
        document.getElementById('offline-time').textContent = data.offline_time;
        document.getElementById('offline-gold').textContent = formatNumber(data.offline_earned);
        document.getElementById('offline-modal').classList.add('show');
        document.getElementById('modal-overlay').classList.add('show');
    }
}

function renderGame() {
    renderHeader();
    renderMineLayers();
    renderPanelContent();
}

function renderHeader() {
    document.getElementById('gold-value').textContent = formatNumber(gameState.user.gold);
    document.getElementById('gem-value').textContent = gameState.gems;
    document.getElementById('cash-value').textContent = formatNumber(gameState.cash);
    document.getElementById('gps-value').textContent = formatNumber(gameState.goldPerSecond);
}

function renderMineLayers() {
    const container = document.getElementById('mine-layers');
    container.innerHTML = '';
    
    const unlockedLayers = gameState.layers.filter(l => l.unlocked);
    
    const helmetColors = ['#FFD700', '#FF9800', '#E91E63', '#9C27B0', '#00BCD4'];
    const bodyColors = ['#4169E1', '#4CAF50', '#9C27B0', '#FF5722', '#009688'];
    
    unlockedLayers.forEach(layer => {
        const miner = gameState.miners[layer.id] || { count: 0, speed: 1, level: 1 };
        const layerGold = layer.base_gold_per_second * miner.count * miner.speed * (layer.efficiency || 1);
        const colorIdx = (layer.layer_depth - 1) % helmetColors.length;
        
        const layerEl = document.createElement('div');
        layerEl.className = `mine-layer ${gameState.selectedLayerId === layer.id ? 'active' : ''}`;
        layerEl.dataset.layerId = layer.id;
        
        layerEl.innerHTML = `
            ${createMinerHTML(helmetColors[colorIdx], bodyColors[colorIdx])}
            ${createOreHTML(layer.layer_depth)}
            <div class="layer-number">${layer.layer_depth}</div>
            <div class="layer-info">
                <div class="layer-name">${layer.name}</div>
                <div class="layer-output">${formatNumber(layerGold)}/秒 · 👷${miner.count}</div>
            </div>
            <div class="layer-actions">
                <button class="btn-hire" onclick="hireMiner(${layer.id})" ${gameState.user.gold < calculateCost(200, miner.count) ? 'disabled' : ''}>
                    雇佣 ${formatNumber(calculateCost(200, miner.count))}
                </button>
                <button class="btn-upgrade" onclick="upgradeMiner(${layer.id})" ${gameState.user.gold < calculateCost(100, miner.level) ? 'disabled' : ''}>
                    升级 ${formatNumber(calculateCost(100, miner.level))}
                </button>
            </div>
        `;
        
        layerEl.addEventListener('click', (e) => {
            if (e.target.tagName === 'BUTTON') return;
            gameState.selectedLayerId = layer.id;
            renderMineLayers();
            renderPanelContent();
        });
        
        container.appendChild(layerEl);
    });
    
    if (gameState.nextLayer) {
        const unlockEl = document.createElement('div');
        unlockEl.className = 'mine-layer locked';
        const nextDepth = gameState.nextLayer.layer_depth;
        unlockEl.innerHTML = `
            <div class="lock-icon">🔒</div>
            ${createOreHTML(nextDepth)}
            <div class="layer-number" style="background:#FF9800;">🔓</div>
            <div class="layer-info">
                <div class="layer-name">解锁第${nextDepth}层</div>
                <div class="layer-output">${gameState.nextLayer.name}</div>
            </div>
            <button class="btn-hire" onclick="unlockNextLayer()" style="width:auto;padding:4px 8px;">
                ${formatNumber(gameState.nextLayer.unlock_cost)}
            </button>
        `;
        container.appendChild(unlockEl);
    }
}

function renderPanelContent() {
    const content = document.getElementById('panel-content');
    const title = document.getElementById('panel-title');
    
    switch (gameState.currentPanel) {
        case 'miners': title.textContent = '矿工管理'; renderMinersPanel(content); break;
        case 'elevator': title.textContent = '电梯管理'; renderElevatorPanel(content); break;
        case 'ground': title.textContent = '地面管理'; renderGroundPanel(content); break;
        case 'mines': title.textContent = '矿山管理'; renderMinesPanel(content); break;
    }
}

function renderMinersPanel(container) {
    const layer = gameState.layers.find(l => l.id === gameState.selectedLayerId);
    const miner = layer ? gameState.miners[layer.id] : null;
    if (!layer || !miner) {
        container.innerHTML = '<p style="text-align:center;color:#888;padding:20px;">选择矿层管理</p>';
        return;
    }
    const colorIdx = (layer.layer_depth - 1) % gameState.oreColors.length;
    const color = getOreColor(layer.layer_depth);
    container.innerHTML = `
        <div class="upgrade-card" onclick="hireMiner(${layer.id})">
            <div class="upgrade-info">
                <div class="upgrade-icon-big" style="background: linear-gradient(135deg, #81D4FA, #0288D1); border-color: #01579B;">👷</div>
                <div class="upgrade-details">
                    <div class="upgrade-name">雇佣矿工</div>
                    <div class="upgrade-desc">当前 ${miner.count} 人</div>
                </div>
            </div>
            <div class="upgrade-cost">${formatNumber(calculateCost(200, miner.count))} 💰</div>
        </div>
        <div class="upgrade-card" onclick="upgradeMiner(${layer.id})">
            <div class="upgrade-info">
                <div class="upgrade-icon-big" style="background: linear-gradient(135deg, #FFD54F, #FF8F00); border-color: #E65100;">⛏️</div>
                <div class="upgrade-details">
                    <div class="upgrade-name">升级矿工</div>
                    <div class="upgrade-desc">Lv.${miner.level} · 速度 ${miner.speed.toFixed(1)}x</div>
                </div>
            </div>
            <div class="upgrade-cost">${formatNumber(calculateCost(100, miner.level))} 💰</div>
        </div>
        <div class="upgrade-card">
            <div class="upgrade-info">
                <div class="upgrade-icon-big" style="background: linear-gradient(135deg, #CE93D8, #7B1FA2); border-color: #4A148C;">👔</div>
                <div class="upgrade-details">
                    <div class="upgrade-name">矿工主管</div>
                    <div class="upgrade-desc">自动管理，提升效率</div>
                </div>
            </div>
            <div class="upgrade-cost">500 💎</div>
        </div>
    `;
}

function renderElevatorPanel(container) {
    container.innerHTML = `
        <div class="upgrade-card" onclick="upgradeElevator()">
            <div class="upgrade-info">
                <div class="upgrade-icon-big" style="background: linear-gradient(135deg, #90A4AE, #455A64); border-color: #263238;">🛗</div>
                <div class="upgrade-details">
                    <div class="upgrade-name">升级电梯</div>
                    <div class="upgrade-desc">Lv.${gameState.elevator.level} · 速度 ${gameState.elevator.speed.toFixed(1)}x</div>
                </div>
            </div>
            <div class="upgrade-cost">${formatNumber(calculateCost(500, gameState.elevator.level))} 💰</div>
        </div>
        <div class="upgrade-card" onclick="hireElevatorWorker()">
            <div class="upgrade-info">
                <div class="upgrade-icon-big" style="background: linear-gradient(135deg, #64B5F6, #1565C0); border-color: #0D47A1;">🧑‍🔧</div>
                <div class="upgrade-details">
                    <div class="upgrade-name">雇佣电梯工</div>
                    <div class="upgrade-desc">当前 ${gameState.elevatorWorker.count} 人</div>
                </div>
            </div>
            <div class="upgrade-cost">${formatNumber(calculateCost(300, gameState.elevatorWorker.count))} 💰</div>
        </div>
        <div class="upgrade-card" onclick="upgradeElevatorWorker()">
            <div class="upgrade-info">
                <div class="upgrade-icon-big" style="background: linear-gradient(135deg, #FFD54F, #FF8F00); border-color: #E65100;">⬆️</div>
                <div class="upgrade-details">
                    <div class="upgrade-name">升级电梯工</div>
                    <div class="upgrade-desc">Lv.${gameState.elevatorWorker.level} · 效率 ${gameState.elevatorWorker.efficiency.toFixed(1)}x</div>
                </div>
            </div>
            <div class="upgrade-cost">${formatNumber(calculateCost(250, gameState.elevatorWorker.level))} 💰</div>
        </div>
        <div class="upgrade-card">
            <div class="upgrade-info">
                <div class="upgrade-icon-big" style="background: linear-gradient(135deg, #CE93D8, #7B1FA2); border-color: #4A148C;">👔</div>
                <div class="upgrade-details">
                    <div class="upgrade-name">电梯主管</div>
                    <div class="upgrade-desc">自动管理，提升运输</div>
                </div>
            </div>
            <div class="upgrade-cost">500 💎</div>
        </div>
    `;
}

function renderGroundPanel(container) {
    container.innerHTML = `
        <div class="upgrade-card" onclick="hireGroundWorker()">
            <div class="upgrade-info">
                <div class="upgrade-icon-big" style="background: linear-gradient(135deg, #81C784, #388E3C); border-color: #1B5E20;">👷‍♂️</div>
                <div class="upgrade-details">
                    <div class="upgrade-name">雇佣地面工</div>
                    <div class="upgrade-desc">当前 ${gameState.groundWorker.count} 人</div>
                </div>
            </div>
            <div class="upgrade-cost">${formatNumber(calculateCost(300, gameState.groundWorker.count))} 💰</div>
        </div>
        <div class="upgrade-card" onclick="upgradeGroundWorker()">
            <div class="upgrade-info">
                <div class="upgrade-icon-big" style="background: linear-gradient(135deg, #FFD54F, #FF8F00); border-color: #E65100;">⬆️</div>
                <div class="upgrade-details">
                    <div class="upgrade-name">升级地面工</div>
                    <div class="upgrade-desc">Lv.${gameState.groundWorker.level} · 效率 ${gameState.groundWorker.efficiency.toFixed(1)}x</div>
                </div>
            </div>
            <div class="upgrade-cost">${formatNumber(calculateCost(250, gameState.groundWorker.level))} 💰</div>
        </div>
        <div class="upgrade-card">
            <div class="upgrade-info">
                <div class="upgrade-icon-big" style="background: linear-gradient(135deg, #CE93D8, #7B1FA2); border-color: #4A148C;">👔</div>
                <div class="upgrade-details">
                    <div class="upgrade-name">地面主管</div>
                    <div class="upgrade-desc">自动管理，提升变现</div>
                </div>
            </div>
            <div class="upgrade-cost">500 💎</div>
        </div>
    `;
}

function renderMinesPanel(container) {
    const mines = [
        { id: 1, name: '初始矿场', icon: '⛰️', cost: 0, bonus: 1.0, color: '#FFD700' },
        { id: 2, name: '铜矿山', icon: '🟠', cost: 10000, bonus: 1.5, color: '#FF8A65' },
        { id: 3, name: '银矿山', icon: '⚪', cost: 100000, bonus: 2.0, color: '#E0E0E0' },
        { id: 4, name: '金矿山', icon: '🟡', cost: 1000000, bonus: 3.0, color: '#FFD700' },
        { id: 5, name: '钻石矿', icon: '💎', cost: 10000000, bonus: 5.0, color: '#64B5F6' }
    ];
    
    let html = '';
    mines.forEach(mine => {
        const isUnlocked = gameState.unlockedMines.some(m => m.id === mine.id);
        const isCurrent = mine.id === gameState.user.current_mine;
        
        html += `<div class="upgrade-card">
            <div class="upgrade-info">
                <div class="upgrade-icon-big" style="background: linear-gradient(135deg, ${mine.color}, ${adjustColor(mine.color, -40)}); border-color: ${adjustColor(mine.color, -60)};">${mine.icon}</div>
                <div class="upgrade-details">
                    <div class="upgrade-name">${mine.name}</div>
                    <div class="upgrade-desc">收益加成 ${mine.bonus}x</div>
                </div>
            </div>
            ${isCurrent ? '<span style="color:#FFD700;font-weight:bold;">当前</span>' : 
              isUnlocked ? `<span style="color:#4CAF50;cursor:pointer;" onclick="switchMine(${mine.id})">切换</span>` : 
              mine.id === gameState.user.current_mine + 1 ? 
              `<span class="upgrade-cost" style="cursor:pointer;" onclick="unlockMine(${mine.id},${mine.cost})">${formatNumber(mine.cost)} 💰</span>` : 
              '<span style="color:#666;">🔒</span>'}
        </div>`;
    });
    container.innerHTML = html;
}

function startElevatorAnimation() {
    const elevator = document.getElementById('elevator-car');
    const leftDoor = document.getElementById('door-left');
    const rightDoor = document.getElementById('door-right');
    const elevatorBody = elevator.querySelector('.elevator-body');
    const layers = gameState.layers.filter(l => l.unlocked);
    if (layers.length === 0 || !elevator) return;
    
    let idx = 0;
    
    function move() {
        if (!gameState.isGameRunning) return;
        
        leftDoor.classList.remove('open-left');
        rightDoor.classList.remove('open-right');
        elevatorBody.classList.remove('worker-visible');
        
        setTimeout(() => {
            const layerHeight = 80;
            const targetY = idx * layerHeight;
            elevator.style.top = targetY + 'px';
            document.getElementById('elevator-floor').textContent = layers[idx].layer_depth + 'F';
            
            const travelTime = 2000 / gameState.elevator.speed;
            
            setTimeout(() => {
                leftDoor.classList.add('open-left');
                rightDoor.classList.add('open-right');
                elevatorBody.classList.add('worker-visible');
                
                const layerEl = document.querySelector(`.mine-layer[data-layer-id="${layers[idx].id}"]`);
                if (layerEl) {
                    const rect = layerEl.getBoundingClientRect();
                    createMiningEffect(rect.left + rect.width / 2, rect.top + rect.height / 2);
                }
                
                setTimeout(() => {
                    idx++;
                    if (idx >= layers.length) idx = 0;
                    move();
                }, 1000 / gameState.elevator.speed);
            }, travelTime);
        }, 300);
    }
    
    move();
}

function startMiningEffects() {
    function trigger() {
        if (!gameState.isGameRunning) return;
        
        const unlockedLayers = gameState.layers.filter(l => l.unlocked);
        unlockedLayers.forEach(layer => {
            const miner = gameState.miners[layer.id];
            if (miner && miner.count > 0 && Math.random() < 0.25) {
                const layerEl = document.querySelector(`.mine-layer[data-layer-id="${layer.id}"]`);
                if (layerEl) {
                    const rect = layerEl.getBoundingClientRect();
                    createMiningEffect(
                        rect.left + 60 + Math.random() * 60,
                        rect.top + rect.height / 2
                    );
                }
            }
        });
        
        setTimeout(trigger, 700);
    }
    trigger();
}

function bindGameEvents() {
    document.getElementById('btn-settings').addEventListener('click', () => {
        document.getElementById('settings-modal').classList.add('show');
        document.getElementById('modal-overlay').classList.add('show');
    });
    
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('show');
                document.getElementById('modal-overlay').classList.remove('show');
            }
        });
    });
    
    document.getElementById('modal-overlay').addEventListener('click', () => {
        document.querySelectorAll('.modal').forEach(m => m.classList.remove('show'));
        document.getElementById('modal-overlay').classList.remove('show');
    });
    
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            gameState.currentPanel = btn.dataset.panel;
            renderPanelContent();
            document.getElementById('upgrade-panel').classList.add('open');
        });
    });
    
    document.getElementById('panel-close').addEventListener('click', () => {
        document.getElementById('upgrade-panel').classList.remove('open');
    });
}

function startGameLoop() {
    gameState.isGameRunning = true;
    let lastTime = Date.now();
    
    function tick() {
        if (!gameState.isGameRunning) return;
        const now = Date.now();
        const delta = (now - lastTime) / 1000;
        lastTime = now;
        
        gameState.user.gold += gameState.goldPerSecond * delta;
        document.getElementById('gold-value').textContent = formatNumber(gameState.user.gold);
        
        if (now - gameState.lastSyncTime > 5000) {
            syncWithServer();
            gameState.lastSyncTime = now;
        }
        requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
}

async function syncWithServer() {
    const result = await api('/game/mine', 'POST');
    if (result.status === 'success' && result.data.new_achievements) {
        result.data.new_achievements.forEach(ach => showToast(`🏆 ${ach.name}`));
    }
}

async function hireMiner(layerId) {
    const miner = gameState.miners[layerId];
    if (gameState.user.gold < calculateCost(200, miner.count)) { showToast('金币不足！'); return; }
    const result = await api('/game/hire_miner', 'POST', { layer_id: layerId });
    if (result.status === 'success') {
        gameState.user.gold = result.data.gold;
        gameState.miners[layerId].count = result.data.count;
        recalculateGPS(); renderGame(); showToast('👷 雇佣成功！');
    }
}

async function upgradeMiner(layerId) {
    const miner = gameState.miners[layerId];
    if (gameState.user.gold < calculateCost(100, miner.level)) { showToast('金币不足！'); return; }
    const result = await api('/game/upgrade_miner', 'POST', { layer_id: layerId });
    if (result.status === 'success') {
        gameState.user.gold = result.data.gold;
        gameState.miners[layerId].level = result.data.level;
        gameState.miners[layerId].speed = result.data.speed;
        recalculateGPS(); renderGame(); showToast('⬆️ 升级成功！');
    }
}

async function upgradeElevator() {
    if (gameState.user.gold < calculateCost(500, gameState.elevator.level)) { showToast('金币不足！'); return; }
    const result = await api('/game/upgrade_elevator', 'POST');
    if (result.status === 'success') {
        gameState.user.gold = result.data.gold;
        gameState.elevator.level = result.data.level;
        gameState.elevator.speed = result.data.speed;
        recalculateGPS(); renderGame(); showToast('🛗 电梯升级！');
    }
}

async function hireElevatorWorker() {
    if (gameState.user.gold < calculateCost(300, gameState.elevatorWorker.count)) { showToast('金币不足！'); return; }
    const result = await api('/game/hire_elevator_worker', 'POST');
    if (result.status === 'success') {
        gameState.user.gold = result.data.gold;
        gameState.elevatorWorker.count = result.data.count;
        recalculateGPS(); renderGame(); showToast('🧑‍🔧 雇佣电梯工！');
    }
}

async function upgradeElevatorWorker() {
    if (gameState.user.gold < calculateCost(250, gameState.elevatorWorker.level)) { showToast('金币不足！'); return; }
    const result = await api('/game/upgrade_elevator_worker', 'POST');
    if (result.status === 'success') {
        gameState.user.gold = result.data.gold;
        gameState.elevatorWorker.level = result.data.level;
        gameState.elevatorWorker.efficiency = result.data.efficiency;
        recalculateGPS(); renderGame(); showToast('⬆️ 电梯工升级！');
    }
}

async function hireGroundWorker() {
    if (gameState.user.gold < calculateCost(300, gameState.groundWorker.count)) { showToast('金币不足！'); return; }
    const result = await api('/game/hire_ground_worker', 'POST');
    if (result.status === 'success') {
        gameState.user.gold = result.data.gold;
        gameState.groundWorker.count = result.data.count;
        recalculateGPS(); renderGame(); showToast('👷‍♂️ 雇佣地面工！');
    }
}

async function upgradeGroundWorker() {
    if (gameState.user.gold < calculateCost(250, gameState.groundWorker.level)) { showToast('金币不足！'); return; }
    const result = await api('/game/upgrade_ground_worker', 'POST');
    if (result.status === 'success') {
        gameState.user.gold = result.data.gold;
        gameState.groundWorker.level = result.data.level;
        gameState.groundWorker.efficiency = result.data.efficiency;
        recalculateGPS(); renderGame(); showToast('⬆️ 地面工升级！');
    }
}

async function unlockNextLayer() {
    if (!gameState.nextLayer) return;
    if (gameState.user.gold < gameState.nextLayer.unlock_cost) { showToast('金币不足！'); return; }
    
    const result = await api('/game/unlock_layer', 'POST', { layer_id: gameState.nextLayer.id });
    if (result.status === 'success') {
        gameState.user.gold = result.data.gold;
        showToast('🎉 矿层解锁！');
        await refreshGameStatus();
    }
}

async function unlockMine(mineId, cost) {
    if (gameState.user.gold < cost) { showToast('金币不足！'); return; }
    const result = await api('/game/unlock_mine', 'POST', { mine_id: mineId });
    if (result.status === 'success') {
        gameState.user.gold = result.data.gold;
        showToast('🏔️ 矿山解锁！');
        await refreshGameStatus();
    }
}

async function switchMine(mineId) {
    gameState.user.current_mine = mineId;
    await refreshGameStatus();
    showToast('✅ 切换矿山');
}

async function refreshGameStatus() {
    const result = await api('/game/status', 'GET');
    if (result.status === 'success') {
        gameState.user = result.data.user;
        gameState.layers = result.data.layers;
        gameState.miners = {};
        result.data.miners.forEach(m => gameState.miners[m.layer_id] = m);
        gameState.nextLayer = result.data.next_layer;
        gameState.goldPerSecond = result.data.gold_per_second;
        gameState.unlockedMines = result.data.unlocked_mines;
        
        const firstUnlocked = gameState.layers.find(l => l.unlocked);
        if (firstUnlocked) gameState.selectedLayerId = firstUnlocked.id;
        
        renderGame();
        startElevatorAnimation();
    }
}

function recalculateGPS() {
    let total = 0;
    gameState.layers.filter(l => l.unlocked).forEach(layer => {
        const miner = gameState.miners[layer.id];
        if (miner && miner.count > 0)
            total += layer.base_gold_per_second * miner.count * miner.speed * (layer.efficiency || 1);
    });
    total *= gameState.elevator.speed * gameState.elevatorWorker.efficiency * gameState.groundWorker.efficiency * gameState.currentMine.bonus_multiplier;
    gameState.goldPerSecond = Math.round(total * 100) / 100;
}

function collectOffline() {
    api('/game/collect_offline', 'POST').then(result => {
        if (result.status === 'success') {
            gameState.user.gold = result.data.current_gold || gameState.user.gold;
            document.getElementById('offline-modal').classList.remove('show');
            document.getElementById('modal-overlay').classList.remove('show');
            showToast(`💰 领取 ${formatNumber(result.data.gold_earned)} 金币！`);
            renderHeader();
        }
    });
}

function toggleMusic() {
    gameState.musicEnabled = !gameState.musicEnabled;
    const audio = document.getElementById('bg-music');
    const btn = document.getElementById('btn-music');
    const settingBtn = document.getElementById('setting-music-btn');
    if (gameState.musicEnabled) { 
        audio.play().catch(() => {}); 
        btn.textContent = '🔊';
        if (settingBtn) settingBtn.textContent = '🔊';
    }
    else { 
        audio.pause(); 
        btn.textContent = '🔇';
        if (settingBtn) settingBtn.textContent = '🔇';
    }
}

function toggleSound() {
    gameState.soundEnabled = !gameState.soundEnabled;
    showToast(gameState.soundEnabled ? '音效开启' : '音效关闭');
}

function logout() {
    if (confirm('确定退出？')) {
        gameState.isGameRunning = false;
        gameState.token = '';
        localStorage.removeItem('miner_token');
        document.getElementById('game-screen').classList.add('hidden');
        document.getElementById('auth-screen').classList.remove('hidden');
    }
}

window.hireMiner = hireMiner;
window.upgradeMiner = upgradeMiner;
window.unlockNextLayer = unlockNextLayer;
window.unlockMine = unlockMine;
window.switchMine = switchMine;
window.collectOffline = collectOffline;
window.toggleMusic = toggleMusic;
window.toggleSound = toggleSound;
window.logout = logout;
