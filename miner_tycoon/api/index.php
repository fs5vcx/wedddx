<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

require_once 'db.php';
require_once 'auth.php';
require_once 'game.php';

$db = Database::getInstance();

$request = $_SERVER['REQUEST_URI'];
$method = $_SERVER['REQUEST_METHOD'];

$path = parse_url($request, PHP_URL_PATH);
$path = str_replace('/api/', '', $path);
$parts = explode('/', $path);

$action = $parts[0] ?? '';

$response = ['status' => 'error', 'message' => '未知操作'];

switch ($action) {
    case 'register':
        if ($method === 'POST') {
            $data = json_decode(file_get_contents('php://input'), true);
            $response = register($data);
        }
        break;
    case 'login':
        if ($method === 'POST') {
            $data = json_decode(file_get_contents('php://input'), true);
            $response = login($data);
        }
        break;
    case 'game':
        $token = $_SERVER['HTTP_AUTHORIZATION'] ?? '';
        $token = str_replace('Bearer ', '', $token);
        $user = verifyToken($token);
        if (!$user) {
            $response = ['status' => 'error', 'message' => '无效的令牌'];
            break;
        }
        $userId = $user['user_id'];
        $subAction = $parts[1] ?? '';
        switch ($subAction) {
            case 'status':
                $response = getGameStatus($userId);
                break;
            case 'mine':
                $response = mine($userId);
                break;
            case 'unlock_layer':
                $data = json_decode(file_get_contents('php://input'), true);
                $response = unlockLayer($userId, $data);
                break;
            case 'upgrade_miner':
                $data = json_decode(file_get_contents('php://input'), true);
                $response = upgradeMiner($userId, $data);
                break;
            case 'hire_miner':
                $data = json_decode(file_get_contents('php://input'), true);
                $response = hireMiner($userId, $data);
                break;
            case 'upgrade_elevator':
                $response = upgradeElevator($userId);
                break;
            case 'hire_elevator_worker':
                $response = hireElevatorWorker($userId);
                break;
            case 'upgrade_elevator_worker':
                $response = upgradeElevatorWorker($userId);
                break;
            case 'hire_ground_worker':
                $response = hireGroundWorker($userId);
                break;
            case 'upgrade_ground_worker':
                $response = upgradeGroundWorker($userId);
                break;
            case 'unlock_mine':
                $data = json_decode(file_get_contents('php://input'), true);
                $response = unlockMine($userId, $data);
                break;
            case 'claim_achievement':
                $data = json_decode(file_get_contents('php://input'), true);
                $response = claimAchievement($userId, $data);
                break;
            case 'collect_offline':
                $response = collectOfflineRewards($userId);
                break;
            default:
                $response = ['status' => 'error', 'message' => '未知的游戏操作'];
        }
        break;
    default:
        $response = ['status' => 'error', 'message' => '无效的请求'];
}

echo json_encode($response);
