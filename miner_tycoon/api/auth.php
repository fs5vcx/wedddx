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
    
    $existing = $db->fetchOne('SELECT id FROM users WHERE username = ?', [$username], 's');
    if ($existing) {
        return ['status' => 'error', 'message' => '用户名已存在'];
    }
    
    $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
    
    $result = $db->execute('INSERT INTO users (username, password) VALUES (?, ?)', [$username, $hashedPassword], 'ss');
    
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
    
    $user = $db->fetchOne('SELECT id, password FROM users WHERE username = ?', [$username], 's');
    
    if (!$user || !password_verify($password, $user['password'])) {
        return ['status' => 'error', 'message' => '用户名或密码错误'];
    }
    
    $db->execute('UPDATE users SET last_online = NOW() WHERE id = ?', [$user['id']], 'i');
    
    $token = generateToken($user['id']);
    
    return ['status' => 'success', 'message' => '登录成功', 'token' => $token, 'user_id' => $user['id']];
}

function generateToken($userId) {
    $payload = [
        'user_id' => $userId,
        'exp' => time() + JWT_EXPIRE
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
    
    $db->execute('INSERT INTO user_layers (user_id, layer_id, unlocked) VALUES (?, 1, 1)', [$userId], 'i');
    $db->execute('INSERT INTO miners (user_id, layer_id, count) VALUES (?, 1, 1)', [$userId], 'i');
    $db->execute('INSERT INTO elevators (user_id) VALUES (?)', [$userId], 'i');
    $db->execute('INSERT INTO elevator_workers (user_id) VALUES (?)', [$userId], 'i');
    $db->execute('INSERT INTO ground_workers (user_id) VALUES (?)', [$userId], 'i');
    
    $achievements = $db->fetchAll('SELECT id FROM achievements');
    foreach ($achievements as $achievement) {
        $db->execute('INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)', [$userId, $achievement['id']], 'ii');
    }
}
