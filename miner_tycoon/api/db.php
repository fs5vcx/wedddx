<?php
require_once __DIR__ . '/../config/config.php';

class Database {
    private static $instance = null;
    private $conn;

    private function __construct() {
        $this->conn = new PDO('sqlite:' . DB_PATH);
        $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $this->conn->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        $this->initTables();
    }

    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    public function getConnection() {
        return $this->conn;
    }

    private function initTables() {
        $sql = "
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            gold REAL DEFAULT 100,
            gems INTEGER DEFAULT 0,
            cash REAL DEFAULT 0,
            current_mine INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_active DATETIME DEFAULT CURRENT_TIMESTAMP,
            offline_earned REAL DEFAULT 0,
            offline_time INTEGER DEFAULT 0,
            offline_collected INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS mines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            unlock_cost REAL DEFAULT 0,
            bonus_multiplier REAL DEFAULT 1.0,
            required_depth INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS user_mines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            mine_id INTEGER NOT NULL,
            unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS mine_layers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mine_id INTEGER NOT NULL,
            layer_depth INTEGER NOT NULL,
            name TEXT NOT NULL,
            base_gold_per_second REAL NOT NULL DEFAULT 1,
            unlock_cost REAL NOT NULL DEFAULT 100,
            efficiency REAL DEFAULT 1.0,
            is_unlocked INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS user_layers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            layer_id INTEGER NOT NULL,
            unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            efficiency REAL DEFAULT 1.0
        );

        CREATE TABLE IF NOT EXISTS miners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            layer_id INTEGER NOT NULL,
            count INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            speed REAL DEFAULT 1.0
        );

        CREATE TABLE IF NOT EXISTS elevators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            level INTEGER DEFAULT 1,
            speed REAL DEFAULT 1.0,
            capacity INTEGER DEFAULT 10
        );

        CREATE TABLE IF NOT EXISTS elevator_workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            count INTEGER DEFAULT 1,
            level INTEGER DEFAULT 1,
            efficiency REAL DEFAULT 1.0
        );

        CREATE TABLE IF NOT EXISTS ground_workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            count INTEGER DEFAULT 1,
            level INTEGER DEFAULT 1,
            efficiency REAL DEFAULT 1.0
        );

        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            condition_type TEXT NOT NULL,
            condition_value REAL NOT NULL,
            reward_gold REAL DEFAULT 0,
            reward_gems INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS user_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            achievement_id INTEGER NOT NULL,
            earned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            claimed INTEGER DEFAULT 0
        );
        ";

        $this->conn->exec($sql);
        $this->seedInitialData();
    }

    private function seedInitialData() {
        $stmt = $this->conn->query("SELECT COUNT(*) as count FROM mines");
        $row = $stmt->fetch();
        if ($row['count'] > 0) return;

        $mines = [
            ['name' => '初始矿场', 'description' => '你的第一座矿山', 'unlock_cost' => 0, 'bonus_multiplier' => 1.0, 'required_depth' => 1],
            ['name' => '铜矿山', 'description' => '富含铜矿的山脉', 'unlock_cost' => 10000, 'bonus_multiplier' => 1.5, 'required_depth' => 5],
            ['name' => '银矿山', 'description' => '闪闪发光的银矿', 'unlock_cost' => 100000, 'bonus_multiplier' => 2.0, 'required_depth' => 10],
            ['name' => '金矿山', 'description' => '传说中的黄金矿脉', 'unlock_cost' => 1000000, 'bonus_multiplier' => 3.0, 'required_depth' => 15],
            ['name' => '钻石矿', 'description' => '价值连城的钻石', 'unlock_cost' => 10000000, 'bonus_multiplier' => 5.0, 'required_depth' => 20]
        ];

        foreach ($mines as $mine) {
            $stmt = $this->conn->prepare("INSERT INTO mines (name, description, unlock_cost, bonus_multiplier, required_depth) VALUES (?, ?, ?, ?, ?)");
            $stmt->execute([$mine['name'], $mine['description'], $mine['unlock_cost'], $mine['bonus_multiplier'], $mine['required_depth']]);
            $mineId = $this->conn->lastInsertId();
            $this->seedMineLayers($mineId);
        }

        $achievements = [
            ['name' => '初出茅庐', 'description' => '赚取第一桶金', 'condition_type' => 'total_gold', 'condition_value' => 1000, 'reward_gold' => 500, 'reward_gems' => 0],
            ['name' => '小有成就', 'description' => '累计赚取10000金币', 'condition_type' => 'total_gold', 'condition_value' => 10000, 'reward_gold' => 5000, 'reward_gems' => 5],
            ['name' => '矿业新贵', 'description' => '累计赚取100000金币', 'condition_type' => 'total_gold', 'condition_value' => 100000, 'reward_gold' => 50000, 'reward_gems' => 20],
            ['name' => '矿工队长', 'description' => '雇佣10名矿工', 'condition_type' => 'total_miners', 'condition_value' => 10, 'reward_gold' => 1000, 'reward_gems' => 10],
            ['name' => '深入地心', 'description' => '解锁第5层', 'condition_type' => 'max_depth', 'condition_value' => 5, 'reward_gold' => 5000, 'reward_gems' => 10],
            ['name' => '黄金帝国', 'description' => '累计赚取1000000金币', 'condition_type' => 'total_gold', 'condition_value' => 1000000, 'reward_gold' => 500000, 'reward_gems' => 100]
        ];

        foreach ($achievements as $ach) {
            $stmt = $this->conn->prepare("INSERT INTO achievements (name, description, condition_type, condition_value, reward_gold, reward_gems) VALUES (?, ?, ?, ?, ?, ?)");
            $stmt->execute([$ach['name'], $ach['description'], $ach['condition_type'], $ach['condition_value'], $ach['reward_gold'], $ach['reward_gems']]);
        }
    }

    private function seedMineLayers($mineId) {
        $layerNames = [
            '表层土矿', '浅层矿脉', '中层岩层', '深层矿洞', '地心矿脉',
            '熔岩矿层', '水晶洞窟', '古代矿场', '神秘矿层', '传说矿脉',
            '深渊矿层', '暗金矿脉', '星尘矿层', '虚空矿洞', '永恒矿脉',
            '混沌矿层', '黎明矿脉', '黄昏矿层', '永恒之井', '创世矿脉'
        ];

        for ($i = 1; $i <= 20; $i++) {
            $name = $layerNames[$i - 1] ?? "第{$i}层";
            $baseGold = pow(1.8, $i - 1) * 0.5;
            $unlockCost = pow(2.5, $i - 1) * 50;

            $stmt = $this->conn->prepare("INSERT INTO mine_layers (mine_id, layer_depth, name, base_gold_per_second, unlock_cost, is_unlocked) VALUES (?, ?, ?, ?, ?, ?)");
            $stmt->execute([$mineId, $i, $name, $baseGold, $unlockCost, $i == 1 ? 1 : 0]);
        }
    }

    public function query($sql, $params = []) {
        try {
            $stmt = $this->conn->prepare($sql);
            $stmt->execute($params);
            return $stmt;
        } catch (PDOException $e) {
            return false;
        }
    }

    public function fetchAll($sql, $params = []) {
        $stmt = $this->query($sql, $params);
        if (!$stmt) return [];
        return $stmt->fetchAll();
    }

    public function fetchOne($sql, $params = []) {
        $stmt = $this->query($sql, $params);
        if (!$stmt) return null;
        $row = $stmt->fetch();
        return $row ?: null;
    }

    public function execute($sql, $params = []) {
        try {
            $stmt = $this->conn->prepare($sql);
            $stmt->execute($params);
            return [
                'affected_rows' => $stmt->rowCount(),
                'insert_id' => $this->conn->lastInsertId()
            ];
        } catch (PDOException $e) {
            return ['error' => $e->getMessage()];
        }
    }
}