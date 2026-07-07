CREATE DATABASE IF NOT EXISTS miner_tycoon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE miner_tycoon;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    gold BIGINT DEFAULT 1000,
    total_gold BIGINT DEFAULT 0,
    current_mine INT DEFAULT 1,
    last_online TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    unlock_cost BIGINT NOT NULL,
    max_depth INT NOT NULL,
    bonus_multiplier DECIMAL(5,2) DEFAULT 1.00,
    description TEXT,
    icon VARCHAR(50) DEFAULT '🏔️'
);

CREATE TABLE IF NOT EXISTS mine_layers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mine_id INT NOT NULL,
    layer_depth INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    base_gold_per_second BIGINT NOT NULL,
    unlock_cost BIGINT NOT NULL,
    ore_type VARCHAR(50) NOT NULL,
    ore_color VARCHAR(20) DEFAULT '#8B4513',
    FOREIGN KEY (mine_id) REFERENCES mines(id)
);

CREATE TABLE IF NOT EXISTS user_layers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    layer_id INT NOT NULL,
    unlocked BOOLEAN DEFAULT FALSE,
    level INT DEFAULT 1,
    efficiency DECIMAL(5,2) DEFAULT 1.00,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (layer_id) REFERENCES mine_layers(id),
    UNIQUE KEY (user_id, layer_id)
);

CREATE TABLE IF NOT EXISTS miners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    layer_id INT NOT NULL,
    count INT DEFAULT 0,
    level INT DEFAULT 1,
    speed DECIMAL(5,2) DEFAULT 1.00,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (layer_id) REFERENCES mine_layers(id),
    UNIQUE KEY (user_id, layer_id)
);

CREATE TABLE IF NOT EXISTS elevators (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    count INT DEFAULT 1,
    level INT DEFAULT 1,
    speed DECIMAL(5,2) DEFAULT 1.00,
    capacity INT DEFAULT 100,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS elevator_workers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    count INT DEFAULT 1,
    level INT DEFAULT 1,
    efficiency DECIMAL(5,2) DEFAULT 1.00,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS ground_workers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    count INT DEFAULT 1,
    level INT DEFAULT 1,
    efficiency DECIMAL(5,2) DEFAULT 1.00,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS upgrades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    upgrade_type ENUM('miner', 'elevator', 'elevator_worker', 'ground_worker', 'layer') NOT NULL,
    target_id INT NOT NULL,
    level INT NOT NULL,
    cost BIGINT NOT NULL,
    effect VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS achievements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50) DEFAULT '🏆',
    reward BIGINT DEFAULT 0,
    condition_type VARCHAR(50) NOT NULL,
    condition_value BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_achievements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    achievement_id INT NOT NULL,
    progress BIGINT DEFAULT 0,
    completed BOOLEAN DEFAULT FALSE,
    claimed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (achievement_id) REFERENCES achievements(id),
    UNIQUE KEY (user_id, achievement_id)
);

CREATE TABLE IF NOT EXISTS game_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO mines (name, unlock_cost, max_depth, bonus_multiplier, description, icon) VALUES
('初始矿场', 0, 5, 1.00, '新手矿工的起点', '⛏️'),
('铜矿山', 10000, 8, 1.50, '富含铜矿的矿山', '🟤'),
('银矿山', 100000, 10, 2.00, '银矿资源丰富', '⬜'),
('金矿山', 1000000, 12, 3.00, '黄金矿脉', '🟡'),
('钻石矿', 10000000, 15, 5.00, '稀有的钻石资源', '💎');

INSERT INTO mine_layers (mine_id, layer_depth, name, base_gold_per_second, unlock_cost, ore_type, ore_color) VALUES
(1, 1, '浅层土层', 10, 0, '泥土', '#8B4513'),
(1, 2, '石层', 25, 500, '石头', '#808080'),
(1, 3, '煤矿层', 50, 2000, '煤矿', '#2F4F4F'),
(1, 4, '铁矿层', 100, 5000, '铁矿', '#708090'),
(1, 5, '宝石层', 200, 10000, '宝石', '#FFD700'),
(2, 1, '铜矿石层', 50, 10000, '铜矿', '#B87333'),
(2, 2, '富铜矿层', 120, 30000, '富铜矿', '#CD7F32'),
(2, 3, '银铜混合层', 250, 80000, '银铜矿', '#C0C0C0'),
(2, 4, '深层铜矿', 500, 200000, '深层铜矿', '#DAA520'),
(2, 5, '稀有矿脉', 1000, 500000, '稀有矿石', '#9370DB'),
(2, 6, '秘银层', 2000, 1000000, '秘银', '#E6E6FA'),
(2, 7, '暗铁矿', 4000, 2500000, '暗铁', '#4682B4'),
(2, 8, '星铁矿', 8000, 5000000, '星铁', '#00CED1'),
(3, 1, '银矿石层', 200, 100000, '银矿', '#C0C0C0'),
(3, 2, '富银矿层', 500, 300000, '富银矿', '#E8E8E8'),
(3, 3, '铂金层', 1000, 800000, '铂金', '#E5E4E2'),
(3, 4, '白银深处', 2000, 2000000, '深层银矿', '#F5F5F5'),
(3, 5, '月光石层', 4000, 5000000, '月光石', '#E6E6FA'),
(3, 6, '冰晶矿', 8000, 10000000, '冰晶', '#ADD8E6'),
(3, 7, '蓝宝石层', 16000, 25000000, '蓝宝石', '#4169E1'),
(3, 8, '紫水晶层', 32000, 50000000, '紫水晶', '#9B59B6'),
(3, 9, '翡翠层', 64000, 100000000, '翡翠', '#00FF7F'),
(3, 10, '红宝石层', 128000, 200000000, '红宝石', '#DC143C'),
(4, 1, '金矿石层', 500, 1000000, '金矿', '#FFD700'),
(4, 2, '富金矿层', 1200, 3000000, '富金矿', '#FFA500'),
(4, 3, '金沙层', 2500, 8000000, '金沙', '#FDB813'),
(4, 4, '黄金深处', 5000, 20000000, '深层金矿', '#FFD700'),
(4, 5, '赤金层', 10000, 50000000, '赤金', '#CD853F'),
(4, 6, '炼金矿', 20000, 100000000, '炼金矿', '#DAA520'),
(4, 7, '真金层', 40000, 250000000, '真金', '#FFC125'),
(4, 8, '龙鳞金', 80000, 500000000, '龙鳞金', '#FFB90F'),
(4, 9, '凤凰金', 160000, 1000000000, '凤凰金', '#FF8C00'),
(4, 10, '神圣金', 320000, 2000000000, '神圣金', '#FFD700'),
(4, 11, '天界金', 640000, 5000000000, '天界金', '#FFFAF0'),
(4, 12, '永恒金', 1280000, 10000000000, '永恒金', '#FFFF00'),
(5, 1, '钻石原石层', 2000, 10000000, '钻石原石', '#B9F2FF'),
(5, 2, '钻石矿层', 5000, 30000000, '钻石', '#E0FFFF'),
(5, 3, '蓝钻石层', 10000, 80000000, '蓝钻', '#87CEEB'),
(5, 4, '粉钻石层', 20000, 200000000, '粉钻', '#FFB6C1'),
(5, 5, '绿钻石层', 40000, 500000000, '绿钻', '#ADFF2F'),
(5, 6, '黑钻石层', 80000, 1000000000, '黑钻', '#1a1a1a'),
(5, 7, '彩虹钻石层', 160000, 2500000000, '彩虹钻', '#FF1493'),
(5, 8, '星光钻石层', 320000, 5000000000, '星光钻', '#E6E6FA'),
(5, 9, '月光钻石层', 640000, 10000000000, '月光钻', '#F0F8FF'),
(5, 10, '太阳钻石层', 1280000, 20000000000, '太阳钻', '#FFD700'),
(5, 11, '永恒钻石层', 2560000, 50000000000, '永恒钻', '#FFFFFF'),
(5, 12, '虚空钻石层', 5120000, 100000000000, '虚空钻', '#4B0082'),
(5, 13, '创世钻石层', 10240000, 250000000000, '创世钻', '#FF00FF'),
(5, 14, '神之钻石层', 20480000, 500000000000, '神之钻', '#00FFFF'),
(5, 15, '宇宙核心', 40960000, 1000000000000, '宇宙核心', '#FFD700');

INSERT INTO upgrades (upgrade_type, target_id, level, cost, effect, description) VALUES
('miner', 0, 1, 100, 'miner_speed+0.2', '矿工速度提升20%'),
('miner', 0, 2, 300, 'miner_speed+0.2', '矿工速度再提升20%'),
('miner', 0, 3, 800, 'miner_speed+0.2', '矿工速度再提升20%'),
('miner', 0, 4, 2000, 'miner_speed+0.2', '矿工速度再提升20%'),
('miner', 0, 5, 5000, 'miner_speed+0.3', '矿工速度提升30%'),
('elevator', 0, 1, 200, 'elevator_speed+0.2', '电梯速度提升20%'),
('elevator', 0, 2, 600, 'elevator_speed+0.2', '电梯速度再提升20%'),
('elevator', 0, 3, 1500, 'elevator_speed+0.2', '电梯速度再提升20%'),
('elevator', 0, 4, 4000, 'elevator_speed+0.2', '电梯速度再提升20%'),
('elevator', 0, 5, 10000, 'elevator_capacity+50', '电梯容量增加50'),
('elevator_worker', 0, 1, 150, 'worker_efficiency+0.2', '电梯工效率提升20%'),
('elevator_worker', 0, 2, 450, 'worker_efficiency+0.2', '电梯工效率再提升20%'),
('elevator_worker', 0, 3, 1200, 'worker_efficiency+0.2', '电梯工效率再提升20%'),
('elevator_worker', 0, 4, 3000, 'worker_efficiency+0.2', '电梯工效率再提升20%'),
('elevator_worker', 0, 5, 8000, 'worker_efficiency+0.3', '电梯工效率提升30%'),
('ground_worker', 0, 1, 150, 'worker_efficiency+0.2', '地面工效率提升20%'),
('ground_worker', 0, 2, 450, 'worker_efficiency+0.2', '地面工效率再提升20%'),
('ground_worker', 0, 3, 1200, 'worker_efficiency+0.2', '地面工效率再提升20%'),
('ground_worker', 0, 4, 3000, 'worker_efficiency+0.2', '地面工效率再提升20%'),
('ground_worker', 0, 5, 8000, 'worker_efficiency+0.3', '地面工效率提升30%');

INSERT INTO achievements (name, description, icon, reward, condition_type, condition_value) VALUES
('初出茅庐', '完成第一次挖矿', '🎯', 100, 'total_gold', 100),
('小矿工', '累计获得1000金币', '💰', 500, 'total_gold', 1000),
('勤奋矿工', '累计获得10000金币', '💪', 2000, 'total_gold', 10000),
('矿业新手', '解锁第3层矿洞', '⛏️', 1000, 'unlocked_layers', 3),
('中层矿工', '解锁第5层矿洞', '🏗️', 5000, 'unlocked_layers', 5),
('资深矿工', '解锁第10层矿洞', '🔧', 20000, 'unlocked_layers', 10),
('电梯操作员', '升级电梯到3级', '🚀', 3000, 'elevator_level', 3),
('运输专家', '雇佣5名电梯工', '👷', 5000, 'elevator_workers', 5),
('销售大师', '雇佣5名地面工', '🤝', 5000, 'ground_workers', 5),
('铜矿大亨', '解锁铜矿山', '🟤', 10000, 'unlocked_mine', 2),
('银矿巨头', '解锁银矿山', '⬜', 50000, 'unlocked_mine', 3),
('金矿霸主', '解锁金矿山', '🟡', 200000, 'unlocked_mine', 4),
('钻石之王', '解锁钻石矿', '💎', 1000000, 'unlocked_mine', 5),
('百万富翁', '累计获得100万金币', '👑', 500000, 'total_gold', 1000000),
('亿万富豪', '累计获得1亿金币', '🏆', 5000000, 'total_gold', 10000000);