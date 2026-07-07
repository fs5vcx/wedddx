<?php
require_once 'db.php';

function getGameStatus($userId) {
    $db = Database::getInstance();
    
    $user = $db->fetchOne('SELECT gold, total_gold, current_mine FROM users WHERE id = ?', [$userId], 'i');
    if (!$user) {
        return ['status' => 'error', 'message' => '用户不存在'];
    }
    
    $currentMine = $db->fetchOne('SELECT * FROM mines WHERE id = ?', [$user['current_mine']], 'i');
    
    $layers = $db->fetchAll('SELECT ml.*, ul.unlocked, ul.level, ul.efficiency 
                            FROM mine_layers ml 
                            LEFT JOIN user_layers ul ON ml.id = ul.layer_id AND ul.user_id = ? 
                            WHERE ml.mine_id = ?', [$userId, $user['current_mine']], 'ii');
    
    $miners = $db->fetchAll('SELECT m.*, ml.layer_depth FROM miners m 
                            LEFT JOIN mine_layers ml ON m.layer_id = ml.id 
                            WHERE m.user_id = ?', [$userId], 'i');
    
    $elevator = $db->fetchOne('SELECT * FROM elevators WHERE user_id = ?', [$userId], 'i');
    $elevatorWorker = $db->fetchOne('SELECT * FROM elevator_workers WHERE user_id = ?', [$userId], 'i');
    $groundWorker = $db->fetchOne('SELECT * FROM ground_workers WHERE user_id = ?', [$userId], 'i');
    
    $unlockedMines = $db->fetchAll('SELECT id, name, icon FROM mines WHERE id <= ?', [$user['current_mine']], 'i');
    
    $achievements = $db->fetchAll('SELECT a.*, ua.progress, ua.completed, ua.claimed 
                                FROM achievements a 
                                JOIN user_achievements ua ON a.id = ua.achievement_id 
                                WHERE ua.user_id = ?', [$userId], 'i');
    
    $nextLayer = $db->fetchOne('SELECT ml.* FROM mine_layers ml 
                                LEFT JOIN user_layers ul ON ml.id = ul.layer_id AND ul.user_id = ? 
                                WHERE ml.mine_id = ? AND ul.unlocked IS NULL 
                                ORDER BY ml.layer_depth ASC LIMIT 1', [$userId, $user['current_mine']], 'ii');
    
    $nextMine = $db->fetchOne('SELECT * FROM mines WHERE id = ?', [$user['current_mine'] + 1], 'i');
    
    $goldPerSecond = calculateGoldPerSecond($userId);
    
    return [
        'status' => 'success',
        'data' => [
            'user' => $user,
            'current_mine' => $currentMine,
            'layers' => $layers,
            'miners' => $miners,
            'elevator' => $elevator,
            'elevator_worker' => $elevatorWorker,
            'ground_worker' => $groundWorker,
            'unlocked_mines' => $unlockedMines,
            'achievements' => $achievements,
            'next_layer' => $nextLayer,
            'next_mine' => $nextMine,
            'gold_per_second' => $goldPerSecond
        ]
    ];
}

function calculateGoldPerSecond($userId) {
    $db = Database::getInstance();
    
    $user = $db->fetchOne('SELECT current_mine FROM users WHERE id = ?', [$userId], 'i');
    $mine = $db->fetchOne('SELECT bonus_multiplier FROM mines WHERE id = ?', [$user['current_mine']], 'i');
    
    $layers = $db->fetchAll('SELECT ml.base_gold_per_second, ul.efficiency 
                            FROM mine_layers ml 
                            JOIN user_layers ul ON ml.id = ul.layer_id 
                            WHERE ul.user_id = ? AND ul.unlocked = 1 AND ml.mine_id = ?', [$userId, $user['current_mine']], 'ii');
    
    $miners = $db->fetchAll('SELECT count, speed, layer_id FROM miners WHERE user_id = ?', [$userId], 'i');
    
    $elevator = $db->fetchOne('SELECT speed FROM elevators WHERE user_id = ?', [$userId], 'i');
    $elevatorWorker = $db->fetchOne('SELECT efficiency FROM elevator_workers WHERE user_id = ?', [$userId], 'i');
    $groundWorker = $db->fetchOne('SELECT efficiency FROM ground_workers WHERE user_id = ?', [$userId], 'i');
    
    $totalGold = 0;
    
    foreach ($layers as $layer) {
        $miner = null;
        foreach ($miners as $m) {
            if ($m['layer_id'] == $layer['id']) {
                $miner = $m;
                break;
            }
        }
        
        if ($miner && $miner['count'] > 0) {
            $miningPower = $layer['base_gold_per_second'] * $miner['count'] * $miner['speed'] * $layer['efficiency'];
            $totalGold += $miningPower;
        }
    }
    
    $totalGold *= $elevator['speed'] * $elevatorWorker['efficiency'] * $groundWorker['efficiency'];
    $totalGold *= $mine['bonus_multiplier'];
    
    return round($totalGold, 2);
}

function mine($userId) {
    $db = Database::getInstance();
    
    $user = $db->fetchOne('SELECT gold, total_gold, current_mine FROM users WHERE id = ?', [$userId], 'i');
    if (!$user) {
        return ['status' => 'error', 'message' => '用户不存在'];
    }
    
    $goldPerSecond = calculateGoldPerSecond($userId);
    $goldEarned = $goldPerSecond / 10;
    
    $newGold = $user['gold'] + $goldEarned;
    $newTotalGold = $user['total_gold'] + $goldEarned;
    
    $db->execute('UPDATE users SET gold = ?, total_gold = ? WHERE id = ?', [$newGold, $newTotalGold, $userId], 'ddi');
    
    checkAchievements($userId, ['total_gold' => $newTotalGold]);
    
    return [
        'status' => 'success',
        'data' => [
            'gold_earned' => round($goldEarned, 2),
            'current_gold' => round($newGold, 2),
            'gold_per_second' => $goldPerSecond
        ]
    ];
}

function unlockLayer($userId, $data) {
    $db = Database::getInstance();
    
    if (!isset($data['layer_id'])) {
        return ['status' => 'error', 'message' => '缺少矿层ID'];
    }
    
    $layer = $db->fetchOne('SELECT * FROM mine_layers WHERE id = ?', [$data['layer_id']], 'i');
    if (!$layer) {
        return ['status' => 'error', 'message' => '矿层不存在'];
    }
    
    $user = $db->fetchOne('SELECT gold, current_mine FROM users WHERE id = ?', [$userId], 'i');
    if ($user['current_mine'] != $layer['mine_id']) {
        return ['status' => 'error', 'message' => '该矿层不属于当前矿山'];
    }
    
    $existing = $db->fetchOne('SELECT unlocked FROM user_layers WHERE user_id = ? AND layer_id = ?', [$userId, $data['layer_id']], 'ii');
    if ($existing && $existing['unlocked']) {
        return ['status' => 'error', 'message' => '矿层已解锁'];
    }
    
    if ($user['gold'] < $layer['unlock_cost']) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $layer['unlock_cost'];
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId], 'di');
    
    if ($existing) {
        $db->execute('UPDATE user_layers SET unlocked = 1 WHERE user_id = ? AND layer_id = ?', [$userId, $data['layer_id']], 'ii');
    } else {
        $db->execute('INSERT INTO user_layers (user_id, layer_id, unlocked) VALUES (?, ?, 1)', [$userId, $data['layer_id']], 'ii');
    }
    
    $db->execute('INSERT INTO miners (user_id, layer_id, count) VALUES (?, ?, 1)', [$userId, $data['layer_id']], 'ii');
    
    $unlockedCount = $db->fetchOne('SELECT COUNT(*) as count FROM user_layers WHERE user_id = ? AND unlocked = 1', [$userId], 'i');
    checkAchievements($userId, ['unlocked_layers' => $unlockedCount['count']]);
    
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
    
    $miner = $db->fetchOne('SELECT * FROM miners WHERE user_id = ? AND layer_id = ?', [$userId, $data['layer_id']], 'ii');
    if (!$miner) {
        return ['status' => 'error', 'message' => '矿工不存在'];
    }
    
    $cost = calculateUpgradeCost($miner['level'], 100);
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId], 'i');
    if ($user['gold'] < $cost) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $cost;
    $newLevel = $miner['level'] + 1;
    $newSpeed = $miner['speed'] + 0.2;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId], 'di');
    $db->execute('UPDATE miners SET level = ?, speed = ? WHERE id = ?', [$newLevel, $newSpeed, $miner['id']], 'iid');
    
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
    
    $miner = $db->fetchOne('SELECT * FROM miners WHERE user_id = ? AND layer_id = ?', [$userId, $data['layer_id']], 'ii');
    if (!$miner) {
        return ['status' => 'error', 'message' => '矿工不存在'];
    }
    
    $cost = calculateUpgradeCost($miner['count'], 200);
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId], 'i');
    if ($user['gold'] < $cost) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $cost;
    $newCount = $miner['count'] + 1;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId], 'di');
    $db->execute('UPDATE miners SET count = ? WHERE id = ?', [$newCount, $miner['id']], 'ii');
    
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
    
    $elevator = $db->fetchOne('SELECT * FROM elevators WHERE user_id = ?', [$userId], 'i');
    if (!$elevator) {
        return ['status' => 'error', 'message' => '电梯不存在'];
    }
    
    $cost = calculateUpgradeCost($elevator['level'], 500);
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId], 'i');
    if ($user['gold'] < $cost) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $cost;
    $newLevel = $elevator['level'] + 1;
    $newSpeed = $elevator['speed'] + 0.2;
    $newCapacity = $elevator['capacity'] + 20;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId], 'di');
    $db->execute('UPDATE elevators SET level = ?, speed = ?, capacity = ? WHERE id = ?', [$newLevel, $newSpeed, $newCapacity, $elevator['id']], 'iidi');
    
    checkAchievements($userId, ['elevator_level' => $newLevel]);
    
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
    
    $worker = $db->fetchOne('SELECT * FROM elevator_workers WHERE user_id = ?', [$userId], 'i');
    if (!$worker) {
        return ['status' => 'error', 'message' => '电梯工不存在'];
    }
    
    $cost = calculateUpgradeCost($worker['count'], 300);
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId], 'i');
    if ($user['gold'] < $cost) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $cost;
    $newCount = $worker['count'] + 1;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId], 'di');
    $db->execute('UPDATE elevator_workers SET count = ? WHERE id = ?', [$newCount, $worker['id']], 'ii');
    
    checkAchievements($userId, ['elevator_workers' => $newCount]);
    
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
    
    $worker = $db->fetchOne('SELECT * FROM elevator_workers WHERE user_id = ?', [$userId], 'i');
    if (!$worker) {
        return ['status' => 'error', 'message' => '电梯工不存在'];
    }
    
    $cost = calculateUpgradeCost($worker['level'], 250);
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId], 'i');
    if ($user['gold'] < $cost) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $cost;
    $newLevel = $worker['level'] + 1;
    $newEfficiency = $worker['efficiency'] + 0.2;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId], 'di');
    $db->execute('UPDATE elevator_workers SET level = ?, efficiency = ? WHERE id = ?', [$newLevel, $newEfficiency, $worker['id']], 'iid');
    
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
    
    $worker = $db->fetchOne('SELECT * FROM ground_workers WHERE user_id = ?', [$userId], 'i');
    if (!$worker) {
        return ['status' => 'error', 'message' => '地面工不存在'];
    }
    
    $cost = calculateUpgradeCost($worker['count'], 300);
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId], 'i');
    if ($user['gold'] < $cost) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $cost;
    $newCount = $worker['count'] + 1;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId], 'di');
    $db->execute('UPDATE ground_workers SET count = ? WHERE id = ?', [$newCount, $worker['id']], 'ii');
    
    checkAchievements($userId, ['ground_workers' => $newCount]);
    
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
    
    $worker = $db->fetchOne('SELECT * FROM ground_workers WHERE user_id = ?', [$userId], 'i');
    if (!$worker) {
        return ['status' => 'error', 'message' => '地面工不存在'];
    }
    
    $cost = calculateUpgradeCost($worker['level'], 250);
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId], 'i');
    if ($user['gold'] < $cost) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $cost;
    $newLevel = $worker['level'] + 1;
    $newEfficiency = $worker['efficiency'] + 0.2;
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId], 'di');
    $db->execute('UPDATE ground_workers SET level = ?, efficiency = ? WHERE id = ?', [$newLevel, $newEfficiency, $worker['id']], 'iid');
    
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
    
    $mine = $db->fetchOne('SELECT * FROM mines WHERE id = ?', [$data['mine_id']], 'i');
    if (!$mine) {
        return ['status' => 'error', 'message' => '矿山不存在'];
    }
    
    $user = $db->fetchOne('SELECT gold, current_mine FROM users WHERE id = ?', [$userId], 'i');
    if ($data['mine_id'] != $user['current_mine'] + 1) {
        return ['status' => 'error', 'message' => '必须按顺序解锁矿山'];
    }
    
    if ($user['gold'] < $mine['unlock_cost']) {
        return ['status' => 'error', 'message' => '金币不足'];
    }
    
    $newGold = $user['gold'] - $mine['unlock_cost'];
    
    $db->execute('UPDATE users SET gold = ?, current_mine = ? WHERE id = ?', [$newGold, $data['mine_id'], $userId], 'dii');
    
    $layer = $db->fetchOne('SELECT id FROM mine_layers WHERE mine_id = ? ORDER BY layer_depth ASC LIMIT 1', [$data['mine_id']], 'i');
    if ($layer) {
        $db->execute('INSERT INTO user_layers (user_id, layer_id, unlocked) VALUES (?, ?, 1)', [$userId, $layer['id']], 'ii');
        $db->execute('INSERT INTO miners (user_id, layer_id, count) VALUES (?, ?, 1)', [$userId, $layer['id']], 'ii');
    }
    
    checkAchievements($userId, ['unlocked_mine' => $data['mine_id']]);
    
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
    
    $userAchievement = $db->fetchOne('SELECT * FROM user_achievements WHERE user_id = ? AND achievement_id = ?', [$userId, $data['achievement_id']], 'ii');
    if (!$userAchievement) {
        return ['status' => 'error', 'message' => '成就不存在'];
    }
    
    if (!$userAchievement['completed']) {
        return ['status' => 'error', 'message' => '成就未完成'];
    }
    
    if ($userAchievement['claimed']) {
        return ['status' => 'error', 'message' => '成就奖励已领取'];
    }
    
    $achievement = $db->fetchOne('SELECT reward FROM achievements WHERE id = ?', [$data['achievement_id']], 'i');
    
    $user = $db->fetchOne('SELECT gold FROM users WHERE id = ?', [$userId], 'i');
    $newGold = $user['gold'] + $achievement['reward'];
    
    $db->execute('UPDATE users SET gold = ? WHERE id = ?', [$newGold, $userId], 'di');
    $db->execute('UPDATE user_achievements SET claimed = 1 WHERE id = ?', [$userAchievement['id']], 'i');
    
    return [
        'status' => 'success',
        'message' => '成就奖励领取成功',
        'data' => [
            'gold' => $newGold,
            'reward' => $achievement['reward']
        ]
    ];
}

function collectOfflineRewards($userId) {
    $db = Database::getInstance();
    
    $user = $db->fetchOne('SELECT last_online, gold, total_gold FROM users WHERE id = ?', [$userId], 'i');
    if (!$user) {
        return ['status' => 'error', 'message' => '用户不存在'];
    }
    
    $lastOnline = strtotime($user['last_online']);
    $now = time();
    $diffSeconds = $now - $lastOnline;
    
    $maxSeconds = OFFLINE_CALCULATION_MAX_HOURS * 3600;
    $effectiveSeconds = min($diffSeconds, $maxSeconds);
    
    if ($effectiveSeconds < 60) {
        return ['status' => 'success', 'message' => '离线时间不足1分钟', 'data' => ['gold_earned' => 0]];
    }
    
    $goldPerSecond = calculateGoldPerSecond($userId);
    $goldEarned = $goldPerSecond * $effectiveSeconds * 0.5;
    
    $newGold = $user['gold'] + $goldEarned;
    $newTotalGold = $user['total_gold'] + $goldEarned;
    
    $db->execute('UPDATE users SET gold = ?, total_gold = ?, last_online = NOW() WHERE id = ?', [$newGold, $newTotalGold, $userId], 'ddi');
    
    return [
        'status' => 'success',
        'message' => '离线奖励领取成功',
        'data' => [
            'gold_earned' => round($goldEarned, 2),
            'offline_time' => floor($effectiveSeconds / 60) . '分钟',
            'current_gold' => round($newGold, 2)
        ]
    ];
}

function checkAchievements($userId, $updates) {
    $db = Database::getInstance();
    
    foreach ($updates as $type => $value) {
        $achievements = $db->fetchAll('SELECT a.id, a.condition_value 
                                    FROM achievements a 
                                    JOIN user_achievements ua ON a.id = ua.achievement_id 
                                    WHERE ua.user_id = ? AND a.condition_type = ? AND ua.completed = 0', [$userId, $type], 'is');
        
        foreach ($achievements as $achievement) {
            if ($value >= $achievement['condition_value']) {
                $db->execute('UPDATE user_achievements SET completed = 1, progress = ? WHERE user_id = ? AND achievement_id = ?', [$value, $userId, $achievement['id']], 'iii');
            }
        }
    }
}

function calculateUpgradeCost($currentLevel, $baseCost) {
    return (int)($baseCost * pow(1.5, $currentLevel - 1));
}
