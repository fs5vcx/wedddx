<?php
require_once '../vendor/autoload<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponent<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resource<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from-><?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId =><?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connection<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data)<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
            return;
        }
        
        $user = $this->verifyToken($data['token']<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
            return;
        }
        
        $user = $this->verifyToken($data['token']);
        
        if (!$user) {
            $conn->send(json_encode(['action' =><?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
            return;
        }
        
        $user = $this->verifyToken($data['token']);
        
        if (!$user) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '无效的令牌']));
            return;
<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
            return;
        }
        
        $user = $this->verifyToken($data['token']);
        
        if (!$user) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '无效的令牌']));
            return;
        }
        
        $userId = $user['user_id'];
        
        if (!isset($this<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
            return;
        }
        
        $user = $this->verifyToken($data['token']);
        
        if (!$user) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '无效的令牌']));
            return;
        }
        
        $userId = $user['user_id'];
        
        if (!isset($this->userConnections[$userId])) {
            $this->userConnections[$userId] = [];<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
            return;
        }
        
        $user = $this->verifyToken($data['token']);
        
        if (!$user) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '无效的令牌']));
            return;
        }
        
        $userId = $user['user_id'];
        
        if (!isset($this->userConnections[$userId])) {
            $this->userConnections[$userId] = [];
        }
        
        $this->userConnections[$userId][] = $conn->resourceId;<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
            return;
        }
        
        $user = $this->verifyToken($data['token']);
        
        if (!$user) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '无效的令牌']));
            return;
        }
        
        $userId = $user['user_id'];
        
        if (!isset($this->userConnections[$userId])) {
            $this->userConnections[$userId] = [];
        }
        
        $this->userConnections[$userId][] = $conn->resourceId;
        
        $conn->send(json_encode(['action' => 'auth_success', 'user_id'<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
            return;
        }
        
        $user = $this->verifyToken($data['token']);
        
        if (!$user) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '无效的令牌']));
            return;
        }
        
        $userId = $user['user_id'];
        
        if (!isset($this->userConnections[$userId])) {
            $this->userConnections[$userId] = [];
        }
        
        $this->userConnections[$userId][] = $conn->resourceId;
        
        $conn->send(json_encode(['action' => 'auth_success', 'user_id' => $userId]));
        
        echo "User {$userId} authenticated on connection {$conn->resource<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
            return;
        }
        
        $user = $this->verifyToken($data['token']);
        
        if (!$user) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '无效的令牌']));
            return;
        }
        
        $userId = $user['user_id'];
        
        if (!isset($this->userConnections[$userId])) {
            $this->userConnections[$userId] = [];
        }
        
        $this->userConnections[$userId][] = $conn->resourceId;
        
        $conn->send(json_encode(['action' => 'auth_success', 'user_id' => $userId]));
        
        echo "User {$userId} authenticated on connection {$conn->resourceId}\n";
    }
    
    public function broadcastToUser($userId, $message)<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
            return;
        }
        
        $user = $this->verifyToken($data['token']);
        
        if (!$user) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '无效的令牌']));
            return;
        }
        
        $userId = $user['user_id'];
        
        if (!isset($this->userConnections[$userId])) {
            $this->userConnections[$userId] = [];
        }
        
        $this->userConnections[$userId][] = $conn->resourceId;
        
        $conn->send(json_encode(['action' => 'auth_success', 'user_id' => $userId]));
        
        echo "User {$userId} authenticated on connection {$conn->resourceId}\n";
    }
    
    public function broadcastToUser($userId, $message) {
        if (!isset($this->userConnections[$userId])) {
            return;
<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
            return;
        }
        
        $user = $this->verifyToken($data['token']);
        
        if (!$user) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '无效的令牌']));
            return;
        }
        
        $userId = $user['user_id'];
        
        if (!isset($this->userConnections[$userId])) {
            $this->userConnections[$userId] = [];
        }
        
        $this->userConnections[$userId][] = $conn->resourceId;
        
        $conn->send(json_encode(['action' => 'auth_success', 'user_id' => $userId]));
        
        echo "User {$userId} authenticated on connection {$conn->resourceId}\n";
    }
    
    public function broadcastToUser($userId, $message) {
        if (!isset($this->userConnections[$userId])) {
            return;
        }
        
        foreach ($this->userConnections[$userId] as $connectionId) {
<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
            return;
        }
        
        $user = $this->verifyToken($data['token']);
        
        if (!$user) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '无效的令牌']));
            return;
        }
        
        $userId = $user['user_id'];
        
        if (!isset($this->userConnections[$userId])) {
            $this->userConnections[$userId] = [];
        }
        
        $this->userConnections[$userId][] = $conn->resourceId;
        
        $conn->send(json_encode(['action' => 'auth_success', 'user_id' => $userId]));
        
        echo "User {$userId} authenticated on connection {$conn->resourceId}\n";
    }
    
    public function broadcastToUser($userId, $message) {
        if (!isset($this->userConnections[$userId])) {
            return;
        }
        
        foreach ($this->userConnections[$userId] as $connectionId) {
            if (isset($this->clients[$connectionId])) {
                $this->clients[$<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
            return;
        }
        
        $user = $this->verifyToken($data['token']);
        
        if (!$user) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '无效的令牌']));
            return;
        }
        
        $userId = $user['user_id'];
        
        if (!isset($this->userConnections[$userId])) {
            $this->userConnections[$userId] = [];
        }
        
        $this->userConnections[$userId][] = $conn->resourceId;
        
        $conn->send(json_encode(['action' => 'auth_success', 'user_id' => $userId]));
        
        echo "User {$userId} authenticated on connection {$conn->resourceId}\n";
    }
    
    public function broadcastToUser($userId, $message) {
        if (!isset($this->userConnections[$userId])) {
            return;
        }
        
        foreach ($this->userConnections[$userId] as $connectionId) {
            if (isset($this->clients[$connectionId])) {
                $this->clients[$connectionId]->send($message);
            }
        }
    }
    
    private function<?php
require_once '../vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

require_once '../config/config.php';
require_once '../api/db.php';

class GameWebSocket implements MessageComponentInterface {
    protected $clients = [];
    protected $userConnections = [];
    
    public function onOpen(ConnectionInterface $conn) {
        $this->clients[$conn->resourceId] = $conn;
        echo "New connection! ({$conn->resourceId})\n";
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg, true);
        
        if (!$data || !isset($data['action'])) {
            return;
        }
        
        switch ($data['action']) {
            case 'authenticate':
                $this->authenticate($from, $data);
                break;
            case 'ping':
                $from->send(json_encode(['action' => 'pong']));
                break;
        }
    }
    
    public function onClose(ConnectionInterface $conn) {
        unset($this->clients[$conn->resourceId]);
        
        foreach ($this->userConnections as $userId => $connectionIds) {
            $key = array_search($conn->resourceId, $connectionIds);
            if ($key !== false) {
                unset($this->userConnections[$userId][$key]);
                if (empty($this->userConnections[$userId])) {
                    unset($this->userConnections[$userId]);
                }
                break;
            }
        }
        
        echo "Connection {$conn->resourceId} has disconnected\n";
    }
    
    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "An error has occurred: {$e->getMessage()}\n";
        $conn->close();
    }
    
    private function authenticate(ConnectionInterface $conn, $data) {
        if (!isset($data['token'])) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '缺少令牌']));
            return;
        }
        
        $user = $this->verifyToken($data['token']);
        
        if (!$user) {
            $conn->send(json_encode(['action' => 'auth_failed', 'message' => '无效的令牌']));
            return;
        }
        
        $userId = $user['user_id'];
        
        if (!isset($this->userConnections[$userId])) {
            $this->userConnections[$userId] = [];
        }
        
        $this->userConnections[$userId][] = $conn->resourceId;
        
        $conn->send(json_encode(['action' => 'auth_success', 'user_id' => $userId]));
        
        echo "User {$userId} authenticated on connection {$conn->resourceId}\n";
    }
    
    public function broadcastToUser($userId, $message) {
        if (!isset($this->userConnections[$userId])) {
            return;
        }
        
        foreach ($this->userConnections[$userId] as $connectionId) {
            if (isset($this->clients[$connectionId])) {
                $this->clients[$connectionId]->send($message);
            }
        }
    }
    
    private function verifyToken($token) {
        if (!$token) {
            return false;
