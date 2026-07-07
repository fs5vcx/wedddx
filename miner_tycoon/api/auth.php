<?php
require_once 'db.php';

function register($data) {
    $db = Database::getInstance();
    
    if (!isset($data['username'], $data['password'])) {
        return ['status' => 'error', 'message' => '缺少用户名或密码'];
    }
    
    $username = trim($data['username']);
    $password = $data['password'];
    
    if (strlen($username) < 3 || strlen($username) > 50) {
        return ['status' => 'error', 'message' => '用户名长度必须在3-50之间'];
    }
    
    if (strlen($password) < 6) {
        return ['status' => 'error', 'message' => '密码长度至少为6位'];
    }
    
    $existing = $db->fetchOne('SELECT id FROM users WHERE username = ?', [$username]);
    if ($existing) {
        return ['status' => 'error', 'message' => '用户名已存在'];
    }
    
    $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
    
    $result = $db->execute('INSERT INTO users (username, password) VALUES (?, ?)', [$username, $hashedPassword]);
    
    if (isset($result['error'])) {
        return ['status' => 'error', 'message' => '注册失败'];
    }
    
    $userId = $result['insert_id'];
    
    initializeGameData($userId);
    
    $token = generateToken($userId);
    
    return ['status' => 'success', 'message' => '注册成功', 'token' => $token, 'user_id' => $userId];
}

function login($data) {
    $db = Database::getInstance();
    
    if (!isset($data['username'], $data['password'])) {
        return ['status' => 'error', 'message' => '缺少用户名或密码'];
    }
    
    $username = trim($data['username']);
    $password = $data['password'];
    
    $user = $db->fetchOne('SELECT id, password FROM users WHERE username = ?', [$username]);
    
    if (!$user || !password_verify($password, $user['password'])) {
        return ['status' => 'error', 'message' => '用户名或密码错误'];
    }
    
    calculateOfflineRewards($user['id']);
    
    $token = generateToken($user['id']);
    
    return ['status' => 'success', 'message' => '登录成功', 'token' => $token, 'user_id' => $user['id']];
}

function calculateOfflineRewards($userId) {
    $db = Database::getInstance();
    
    $user = $db->fetchOne('SELECT * FROM users WHERE id = ?', [$userId]);
    if (!$user) return;
    
    $lastActive = strtotime($user['last_active']);
    $now = time();
    $offlineSeconds = $now - $lastActive;
    
    if ($offlineSeconds < 60) return;
    
    $maxSeconds = OFFLINE_CALCULATION_MAX_HOURS * 3600;
    $offlineSeconds = min($offlineSeconds, $maxSeconds);
    
    $gps = calculateGoldPerSecond($userId);
    $offlineEarned = $gps * $offlineSeconds * 0.5;
    
    if ($offlineEarned > 0) {
        $db->execute('UPDATE users SET offline_earned = ?, offline_time = ?, offline_collected = 0, last_active = datetime(\'now\') WHERE id = ?',
            [$offlineEarned, floor($offlineSeconds / 60), $userId]);
    } else {
        $db->execute('UPDATE users SET last_active = datetime(\'now\') WHERE id = ?', [$userId]);
    }
}

function generateToken($userId) {
    $payload = [
        'user_id' => $userId,
        'exp' => time() + JWT_EXPIRE * 24 * 30
    ];
    $header = json_encode(['alg' => 'HS256', 'typ' => 'JWT']);
    $payload = json_encode($payload);
    
    $header = base64UrlEncode($header);
    $payload = base64UrlEncode($payload);
    
    $signature = hash_hmac('sha256', "$header.$payload", JWT_SECRET, true);
    $signature = base64UrlEncode($signature);
    
    return "$header.$payload.$signature";
}

function verifyToken($token) {
    if (!$token) {
        return false;
    }
    
    $parts = explode('.', $token);
    if (count($parts) !== 3) {
        return false;
    }
    
    list($header, $payload, $signature) = $parts;
    
    $validSignature = hash_hmac('sha256', "$header.$payload", JWT_SECRET, true);
    $validSignature = base64UrlEncode($validSignature);
    
    if ($signature !== $validSignature) {
        return false;
    }
    
    $payload = json_decode(base64UrlDecode($payload), true);
    
    if (isset($payload['exp']) && $payload['exp'] < time()) {
        return false;
    }
    
    return $payload;
}

function base64UrlEncode($data) {
    return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
}

function base64UrlDecode($data) {
    return base64_decode(str_pad(strtr($data, '-_', '+/'), strlen($data) % 4, '=', STR_PAD_RIGHT));
}

function initializeGameData($userId) {
    $db = Database::getInstance();
    
    $firstLayer = $db->fetchOne('SELECT id FROM mine_layers WHERE mine_id = 1 AND layer_depth = 1');
    
    if ($firstLayer) {
        $db->execute('INSERT INTO user_layers (user_id, layer_id) VALUES (?, ?)', [$userId, $firstLayer['id']]);
        $db->execute('INSERT INTO miners (user_id, layer_id, count) VALUES (?, ?, 1)', [$userId, $firstLayer['id']]);
    }
    
    $db->execute('INSERT INTO user_mines (user_id, mine_id) VALUES (?, 1)', [$userId]);
    $db->execute('INSERT INTO elevators (user_id) VALUES (?)', [$userId]);
    $db->execute('INSERT INTO elevator_workers (user_id) VALUES (?)', [$userId]);
    $db->execute('INSERT INTO ground_workers (user_id) VALUES (?)', [$userId]);
    
    $achievements = $db->fetchAll('SELECT id FROM achievements');
    foreach ($achievements as $achievement) {
        $db->execute('INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)', [$userId, $achievement['id']]);
    }
}

function calculateGoldPerSecond($userId) {
    $db = Database::getInstance();
    
    $user = $db->fetchOne('SELECT * FROM users WHERE id = ?', [$userId]);
    $mine = $db->fetchOne('SELECT * FROM mines WHERE id = ?', [$user['current_mine']]);
    
    $layers = $db->fetchAll('
        SELECT ml.*, ul.efficiency as user_efficiency 
        FROM mine_layers ml 
        JOIN user_layers ul ON ml.id = ul.layer_id 
        WHERE ul.user_id = ? AND ml.mine_id = ?
    ', [$userId, $user['current_mine']]);
    
    $total = 0;
    foreach ($layers as $layer) {
        $miner = $db->fetchOne('SELECT * FROM miners WHERE user_id = ? AND layer_id = ?', [$userId, $layer['id']]);
        if ($miner && $miner['count'] > 0) {
            $efficiency = $layer['efficiency'] * ($layer['user_efficiency'] ?? 1);
            $total += $layer['base_gold_per_second'] * $miner['count'] * $miner['speed'] * $efficiency;
        }
    }
    
    $elevator = $db->fetchOne('SELECT * FROM elevators WHERE user_id = ?', [$userId]);
    $ew = $db->fetchOne('SELECT * FROM elevator_workers WHERE user_id = ?', [$userId]);
    $gw = $db->fetchOne('SELECT * FROM ground_workers WHERE user_id = ?', [$userId]);
    
    if ($elevator) $total *= $elevator['speed'];
    if ($ew) $total *= $ew['efficiency'];
    if ($gw) $total *= $gw['efficiency'];
    if ($mine) $total *= $mine['bonus_multiplier'];
    
    return $total;
}