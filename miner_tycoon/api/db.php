<?php
require_once '../config/config.php';

class Database {
    private static $instance = null;
    private $conn;

    private function __construct() {
        $this->conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
        if ($this->conn->connect_error) {
            die("数据库连接失败: " . $this->conn->connect_error);
        }
        $this->conn->set_charset('utf8mb4');
    }

    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new Database();
        }
        return self::$instance;
    }

    public function getConnection() {
        return $this->conn;
    }

    public function query($sql, $params = [], $types = '') {
        $stmt = $this->conn->prepare($sql);
        if (!$stmt) {
            return ['error' => $this->conn->error];
        }
        if (!empty($params)) {
            $stmt->bind_param($types, ...$params);
        }
        $stmt->execute();
        $result = $stmt->get_result();
        $stmt->close();
        return $result;
    }

    public function execute($sql, $params = [], $types = '') {
        $stmt = $this->conn->prepare($sql);
        if (!$stmt) {
            return ['error' => $this->conn->error];
        }
        if (!empty($params)) {
            $stmt->bind_param($types, ...$params);
        }
        $stmt->execute();
        $affectedRows = $stmt->affected_rows;
        $insertId = $stmt->insert_id;
        $stmt->close();
        return ['affected_rows' => $affectedRows, 'insert_id' => $insertId];
    }

    public function fetchAll($sql, $params = [], $types = '') {
        $result = $this->query($sql, $params, $types);
        if (isset($result['error'])) {
            return $result;
        }
        $data = [];
        while ($row = $result->fetch_assoc()) {
            $data[] = $row;
        }
        return $data;
    }

    public function fetchOne($sql, $params = [], $types = '') {
        $result = $this->query($sql, $params, $types);
        if (isset($result['error'])) {
            return $result;
        }
        return $result->fetch_assoc();
    }
}
