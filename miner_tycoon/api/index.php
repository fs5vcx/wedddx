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
        $subAction = $parts[1] ?? '';
        switch ($subAction) {
            case 'status':
                $response = getGameStatus($user['id']);
                break;
            case 'mine':
                $response = mine($user['id']);
                break;
            case 'unlock_layer':
                $data = json_decode(file_get_contents('php://input'), true);
                $response = unlockLayer($user['id'], $data);
                break;
            case 'upgrade_miner':
                $data = json_decode(file_get_contents('php://input'), true);
                $response = upgradeMiner($user['id'], $data);
                break;
            case 'hire_miner':
                $data = json_decode(file_get_contents('php://input'), true);
                $response = hireMiner($user['id'], $data);
                break;
            case 'upgrade_elevator':
                $response = upgradeElevator($user['id']);
                break;
            case 'hire_elevator_worker':
                $response = hireElevatorWorker($user['id']);
                break;
            case 'upgrade_elevator_worker':
                $response = upgradeElevatorWorker($user['id']);
                break;
            case 'hire_ground_worker':
                $response = hireGroundWorker($user['id']);
                break;
            case 'upgrade_ground_worker':
                $response = upgradeGroundWorker($user['id']);
                break;
            case 'unlock_mine':
                $data = json_decode(file_get_contents('php://input'), true);
                $response = unlockMine($user['id'], $data);
                break;
            case 'claim_achievement':
                $data = json_decode(file_get_contents('php://input'), true);
                $response = claimAchievement($user['id'], $data);
                break;
            case 'collect_offline':
                $response = collectOfflineRewards($user['id']);
                break;
            default:
                $response = ['status' => 'error', 'message' => '未知的游戏操作'];
        }
        break;
    default:
        $response = ['status' => 'error', 'message' => '无效的请求'];
}

echo json_encode($response);
