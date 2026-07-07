<?php
require_once 'db.php';
require_once 'auth.php';

function getGameStatus($userId) {
    $db = Database::getInstance();
    
    $user = $db->fetchOne('SELECT * FROM users WHERE id = ?', [$userId]);
    if (!$user) {
        return ['status' => 'error', 'message' => '用户不存在'];
    }
    
    $currentMine = $db->fetchOne('SELECT * FROM mines WHERE id = ?', [$user['current_mine']]);
    
    $layers = $db->fetchAll('
        SELECT ml.*, ul.efficiency as user_efficiency 
        FROM mine_layers ml 
        LEFT JOIN user_layers ul ON ml.id = ul.layer_id AND ul.user_id = ? 
        WHERE ml.mine_id = ?
        ORDER BY ml.layer_depth ASC
    ', [$userId, $user['current_mine']]);
    
    $unlockedLayerIds = [];
    foreach ($layers as $layer) {
        if ($layer['user_efficiency'] !== null) {
            $unlockedLayerIds[] = $layer['id'];
        }
    }
    
    $miners = [];
    if (!empty($unlockedLayerIds)) {
        $placeholders = implode(',', array_fill(0, count($unlockedLayerIds), '?'));
        $miners = $db->fetchAll("
            SELECT m.*, ml.layer_depth 
            FROM miners m 
            LEFT JOIN mine_layers ml ON m.layer_id = ml.id 
            WHERE m.user_id = ? AND m.layer_id IN ($placeholders)
        ", array_merge([$userId], $unlockedLayerIds));
    }
    
    $processedLayers = [];
    $nextLayer = null;
    foreach ($layers as $layer) {
        $layer['unlocked'] = $layer['user_efficiency'] !== null;
        $layer['efficiency'] = $layer['user_efficiency'] ?? $layer['efficiency'];
        $processedLayers[] = $layer;
        if ($layer['user_efficiency'] === null && $nextLayer === null) {
            $nextLayer = $layer;
        }
    }
    
    $elevator = $db->fetchOne('SELECT * FROM elevators WHERE user_id = ?', [$userId]);
    $elevatorWorker = $db->fetchOne('SELECT * FROM elevator_workers WHERE user_id = ?', [$userId]);
    $groundWorker = $db->fetchOne('SELECT * FROM ground_workers WHERE user_id = ?', [$userId]);
    
    $unlockedMines = $db->fetchAll('
        SELECT m.* 
        FROM mines m 
        JOIN user_mines um ON m.id = um.mine_id 
        WHERE um.user_id = ?
    ', [$userId]);
    
    $goldPerSecond = calculateGoldPerSecond($userId);
    
    $offlineEarned = 0;
    $offlineTime = 0;
    if (!$user['offline_collected'] && $user['offline_earned'] > 0) {
        $offlineEarned = $user['offline_earned'];
        $offlineTime = $user['offline_time'];
    }
    
    $db->execute('UPDATE users SET last_active = datetime(\'now\') WHERE id = ?', [$userId]);
    
    return [
        'status' => 'success',
        'data' => [
            'user' => $user,
            'current_mine' => $currentMine,
            'layers' => $processedLayers,
            'miners' => $miners,
            'elevator' => $elevator,
            'elevator_worker' => $elevatorWorker,
            'ground_worker' => $groundWorker,
            'unlocked_mines' => $unlockedMines,
            'next_layer' => $nextLayer,
            'gold_per_second' => round($goldPerSecond, 2),
            'offline_earned' => $offlineEarned,
            'offline_time' => $offlineTime
        ]
    ];
}

function mine($userId) {
    $db = Database::getInstance();
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId]);
    if (!$user) {
        return ['status' => 'error', 'message' => '用户不存在'];
    }
    
    $goldPerSecond = calculateGoldPerSecond($userId);
    $goldEarned = $goldPerSecond / 2;
    
    $newGold = $user['gold'] + $goldEarned;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId]);
    
    $newAchievements = checkAchievements($userId);
    
    return [
        'status' => 'success',
        'data' => [
            'gold_earned' => round($goldEarned, 2),
            'current_gold' => round($newGold, 2),
            'gold_per_second' => $goldPerSecond,
            'new_achievements' => $newAchievements
        ]
    ];
}

function unlockLayer($userId, $data) {
    $db = Database::getInstance();
    
    if (!isset($data['layer_id'])) {
        return ['status' => 'error', 'message' => '缺少矿层ID'];
    }
    
    $layer = $db->fetchOne('SELECT * FROM mine_layers WHERE id = ?', [$data['layer_id']]);
    if (!$layer) {
        return ['status' => 'error', 'message' => '矿层不存在'];
    }
    
    $user = $db->fetchOne('SELECT gold, current_mine FROM users WHERE id = ?', [$userId]);
    if ($user['current_mine'] != $layer['mine_id']) {
        return ['status' => 'error', 'message' => '该矿层不属于当前矿山'];
    }
    
    $existing = $db->fetchOne('SELECT * FROM user_layers WHERE user_id = ? AND layer_id = ?', [$userId, $data['layer_id']]);
    if ($existing) {
        return ['status' => 'error', 'message' => '矿层已解锁'];
    }
    
    if ($user['gold'] < $layer['unlock_cost']) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $layer['unlock_cost'];
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId]);
    
    $db->execute('INSERT INTO user_layers (user_id, layer_id) VALUES (?, ?)', [$userId, $data['layer_id']]);
    $db->execute('INSERT INTO miners (user_id, layer_id, count) VALUES (?, ?, 1)', [$userId, $data['layer_id']]);
    
    return [
        'status' => 'success',
        'message' => '矿层解锁成功',
        'data' => [
            'gold' => $newGold,
            'layer_id' => $data['layer_id']
        ]
    ];
}

function upgradeMiner($userId, $data) {
    $db = Database::getInstance();
    
    if (!isset($data['layer_id'])) {
        return ['status' => 'error', 'message' => '缺少矿层ID'];
    }
    
    $miner = $db->fetchOne('SELECT * FROM miners WHERE user_id = ? AND layer_id = ?', [$userId, $data['layer_id']]);
    if (!$miner) {
        return ['status' => 'error', 'message' => '矿工不存在'];
    }
    
    $cost = calculateUpgradeCost($miner['level'], 100);
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId]);
    if ($user['gold'] < $cost) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $cost;
    $newLevel = $miner['level'] + 1;
    $newSpeed = $miner['speed'] + 0.2;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId]);
    $db->execute('UPDATE miners SET level = ?, speed = ? WHERE id = ?', [$newLevel, $newSpeed, $miner['id']]);
    
    return [
        'status' => 'success',
        'message' => '矿工升级成功',
        'data' => [
            'gold' => $newGold,
            'level' => $newLevel,
            'speed' => round($newSpeed, 2)
        ]
    ];
}

function hireMiner($userId, $data) {
    $db = Database::getInstance();
    
    if (!isset($data['layer_id'])) {
        return ['status' => 'error', 'message' => '缺少矿层ID'];
    }
    
    $miner = $db->fetchOne('SELECT * FROM miners WHERE user_id = ? AND layer_id = ?', [$userId, $data['layer_id']]);
    if (!$miner) {
        return ['status' => 'error', 'message' => '矿工不存在'];
    }
    
    $cost = calculateUpgradeCost($miner['count'], 200);
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId]);
    if ($user['gold'] < $cost) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $cost;
    $newCount = $miner['count'] + 1;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId]);
    $db->execute('UPDATE miners SET count = ? WHERE id = ?', [$newCount, $miner['id']]);
    
    return [
        'status' => 'success',
        'message' => '雇佣矿工成功',
        'data' => [
            'gold' => $newGold,
            'count' => $newCount
        ]
    ];
}

function upgradeElevator($userId) {
    $db = Database::getInstance();
    
    $elevator = $db->fetchOne('SELECT * FROM elevators WHERE user_id = ?', [$userId]);
    if (!$elevator) {
        return ['status' => 'error', 'message' => '电梯不存在'];
    }
    
    $cost = calculateUpgradeCost($elevator['level'], 500);
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId]);
    if ($user['gold'] < $cost) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $cost;
    $newLevel = $elevator['level'] + 1;
    $newSpeed = $elevator['speed'] + 0.2;
    $newCapacity = $elevator['capacity'] + 20;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId]);
    $db->execute('UPDATE elevators SET level = ?, speed = ?, capacity = ? WHERE id = ?', [$newLevel, $newSpeed, $newCapacity, $elevator['id']]);
    
    return [
        'status' => 'success',
        'message' => '电梯升级成功',
        'data' => [
            'gold' => $newGold,
            'level' => $newLevel,
            'speed' => round($newSpeed, 2),
            'capacity' => $newCapacity
        ]
    ];
}

function hireElevatorWorker($userId) {
    $db = Database::getInstance();
    
    $worker = $db->fetchOne('SELECT * FROM elevator_workers WHERE user_id = ?', [$userId]);
    if (!$worker) {
        return ['status' => 'error', 'message' => '电梯工不存在'];
    }
    
    $cost = calculateUpgradeCost($worker['count'], 300);
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId]);
    if ($user['gold'] < $cost) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $cost;
    $newCount = $worker['count'] + 1;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId]);
    $db->execute('UPDATE elevator_workers SET count = ? WHERE id = ?', [$newCount, $worker['id']]);
    
    return [
        'status' => 'success',
        'message' => '雇佣电梯工成功',
        'data' => [
            'gold' => $newGold,
            'count' => $newCount
        ]
    ];
}

function upgradeElevatorWorker($userId) {
    $db = Database::getInstance();
    
    $worker = $db->fetchOne('SELECT * FROM elevator_workers WHERE user_id = ?', [$userId]);
    if (!$worker) {
        return ['status' => 'error', 'message' => '电梯工不存在'];
    }
    
    $cost = calculateUpgradeCost($worker['level'], 250);
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId]);
    if ($user['gold'] < $cost) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $cost;
    $newLevel = $worker['level'] + 1;
    $newEfficiency = $worker['efficiency'] + 0.2;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId]);
    $db->execute('UPDATE elevator_workers SET level = ?, efficiency = ? WHERE id = ?', [$newLevel, $newEfficiency, $worker['id']]);
    
    return [
        'status' => 'success',
        'message' => '电梯工升级成功',
        'data' => [
            'gold' => $newGold,
            'level' => $newLevel,
            'efficiency' => round($newEfficiency, 2)
        ]
    ];
}

function hireGroundWorker($userId) {
    $db = Database::getInstance();
    
    $worker = $db->fetchOne('SELECT * FROM ground_workers WHERE user_id = ?', [$userId]);
    if (!$worker) {
        return ['status' => 'error', 'message' => '地面工不存在'];
    }
    
    $cost = calculateUpgradeCost($worker['count'], 300);
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId]);
    if ($user['gold'] < $cost) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $cost;
    $newCount = $worker['count'] + 1;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId]);
    $db->execute('UPDATE ground_workers SET count = ? WHERE id = ?', [$newCount, $worker['id']]);
    
    return [
        'status' => 'success',
        'message' => '雇佣地面工成功',
        'data' => [
            'gold' => $newGold,
            'count' => $newCount
        ]
    ];
}

function upgradeGroundWorker($userId) {
    $db = Database::getInstance();
    
    $worker = $db->fetchOne('SELECT * FROM ground_workers WHERE user_id = ?', [$userId]);
    if (!$worker) {
        return ['status' => 'error', 'message' => '地面工不存在'];
    }
    
    $cost = calculateUpgradeCost($worker['level'], 250);
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId]);
    if ($user['gold'] < $cost) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $cost;
    $newLevel = $worker['level'] + 1;
    $newEfficiency = $worker['efficiency'] + 0.2;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId]);
    $db->execute('UPDATE ground_workers SET level = ?, efficiency = ? WHERE id = ?', [$newLevel, $newEfficiency, $worker['id']]);
    
    return [
        'status' => 'success',
        'message' => '地面工升级成功',
        'data' => [
            'gold' => $newGold,
            'level' => $newLevel,
            'efficiency' => round($newEfficiency, 2)
        ]
    ];
}

function unlockMine($userId, $data) {
    $db = Database::getInstance();
    
    if (!isset($data['mine_id'])) {
        return ['status' => 'error', 'message' => '缺少矿山ID'];
    }
    
    $mine = $db->fetchOne('SELECT * FROM mines WHERE id = ?', [$data['mine_id']]);
    if (!$mine) {
        return ['status' => 'error', 'message' => '矿山不存在'];
    }
    
    $user = $db->fetchOne('SELECT gold, current_mine FROM users WHERE id = ?', [$userId]);
    
    $existing = $db->fetchOne('SELECT * FROM user_mines WHERE user_id = ? AND mine_id = ?', [$userId, $data['mine_id']]);
    if ($existing) {
        return ['status' => 'error', 'message' => '矿山已解锁'];
    }
    
    if ($user['gold'] < $mine['unlock_cost']) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $mine['unlock_cost'];
    
    $db->execute('UPDATE users SET gold = ?, current_mine = ? WHERE id = ?', [$newGold, $data['mine_id'], $userId]);
    $db->execute('INSERT INTO user_mines (user_id, mine_id) VALUES (?, ?)', [$userId, $data['mine_id']]);
    
    $layer = $db->fetchOne('SELECT id FROM mine_layers WHERE mine_id = ? ORDER BY layer_depth ASC LIMIT 1', [$data['mine_id']]);
    if ($layer) {
        $db->execute('INSERT INTO user_layers (user_id, layer_id) VALUES (?, ?)', [$userId, $layer['id']]);
        $db->execute('INSERT INTO miners (user_id, layer_id, count) VALUES (?, ?, 1)', [$userId, $layer['id']]);
    }
    
    return [
        'status' => 'success',
        'message' => '矿山解锁成功',
        'data' => [
            'gold' => $newGold,
            'mine_id' => $data['mine_id']
        ]
    ];
}

function claimAchievement($userId, $data) {
    $db = Database::getInstance();
    
    if (!isset($data['achievement_id'])) {
        return ['status' => 'error', 'message' => '缺少成就ID'];
    }
    
    $userAchievement = $db->fetchOne('SELECT * FROM user_achievements WHERE user_id = ? AND achievement_id = ?', [$userId, $data['achievement_id']]);
    if (!$userAchievement) {
        return ['status' => 'error', 'message' => '成就不存在'];
    }
    
    if ($userAchievement['claimed']) {
        return ['status' => 'error', 'message' => '成就奖励已领取'];
    }
    
    $achievement = $db->fetchOne('SELECT * FROM achievements WHERE id = ?', [$data['achievement_id']]);
    
    $user = $db->fetchOne('SELECT gold, gems FROM users WHERE id = ?', [$userId]);
    $newGold = $user['gold'] + $achievement['reward_gold'];
    $newGems = $user['gems'] + $achievement['reward_gems'];
    
    $db->execute('UPDATE users SET gold = ?, gems = ? WHERE id = ?', [$newGold, $newGems, $userId]);
    $db->execute('UPDATE user_achievements SET claimed = 1 WHERE id = ?', [$userAchievement['id']]);
    
    return [
        'status' => 'success',
        'message' => '成就奖励领取成功',
        'data' => [
            'gold' => $newGold,
            'gems' => $newGems,
            'reward_gold' => $achievement['reward_gold'],
            'reward_gems' => $achievement['reward_gems']
        ]
    ];
}

function collectOfflineRewards($userId) {
    $db = Database::getInstance();
    
    $user = $db->fetchOne('SELECT * FROM users WHERE id = ?', [$userId]);
    if (!$user) {
        return ['status' => 'error', 'message' => '用户不存在'];
    }
    
    $goldEarned = $user['offline_earned'];
    $newGold = $user['gold'] + $goldEarned;
    
    $db->execute('UPDATE users SET gold = ?, offline_collected = 1, offline_earned = 0 WHERE id = ?', [$newGold, $userId]);
    
    return [
        'status' => 'success',
        'message' => '离线奖励领取成功',
        'data' => [
            'gold_earned' => round($goldEarned, 2),
            'offline_time' => $user['offline_time'] . '分钟',
            'current_gold' => round($newGold, 2)
        ]
    ];
}

function checkAchievements($userId) {
    $db = Database::getInstance();
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId]);
    
    $totalMiners = $db->fetchOne('SELECT SUM(count) as total FROM miners WHERE user_id = ?', [$userId]);
    $totalMiners = $totalMiners['total'] ?? 0;
    
    $maxDepth = $db->fetchOne('
        SELECT MAX(ml.layer_depth) as max_depth 
        FROM user_layers ul 
        JOIN mine_layers ml ON ul.layer_id = ml.id 
        WHERE ul.user_id = ?
    ', [$userId]);
    $maxDepth = $maxDepth['max_depth'] ?? 0;
    
    $conditions = [
        'total_gold' => $user['gold'],
        'total_miners' => $totalMiners,
        'max_depth' => $maxDepth
    ];
    
    $newAchievements = [];
    
    foreach ($conditions as $type => $value) {
        $achievements = $db->fetchAll('
            SELECT a.* 
            FROM achievements a 
            JOIN user_achievements ua ON a.id = ua.achievement_id 
            WHERE ua.user_id = ? AND a.condition_type = ? AND ua.claimed = 0
        ', [$userId, $type]);
        
        foreach ($achievements as $ach) {
            if ($value >= $ach['condition_value']) {
                $ua = $db->fetchOne('
                    SELECT * FROM user_achievements 
                    WHERE user_id = ? AND achievement_id = ?
                ', [$userId, $ach['id']]);
                
                if ($ua) {
                    $newAchievements[] = $ach;
                }
            }
        }
    }
    
    return $newAchievements;
}

function calculateUpgradeCost($currentLevel, $baseCost) {
    return (int)($baseCost * pow(1.5, $currentLevel - 1));
}