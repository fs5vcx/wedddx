<?php
$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$baseDir = __DIR__;

if ($uri === '/' || $uri === '/index.html') {
    require $baseDir . '/frontend/index.html';
    return true;
}

if (strpos($uri, '/api/') === 0) {
    require $baseDir . '/api/index.php';
    return true;
}

$frontendFile = $baseDir . '/frontend' . $uri;
if (file_exists($frontendFile) && is_file($frontendFile)) {
    $ext = pathinfo($frontendFile, PATHINFO_EXTENSION);
    $mimeTypes = [
        'html' => 'text/html',
        'css' => 'text/css',
        'js' => 'application/javascript',
        'json' => 'application/json',
        'png' => 'image/png',
        'jpg' => 'image/jpeg',
        'gif' => 'image/gif',
        'svg' => 'image/svg+xml',
        'ico' => 'image/x-icon',
        'mp3' => 'audio/mpeg',
        'wav' => 'audio/wav'
    ];
    
    if (isset($mimeTypes[$ext])) {
        header('Content-Type: ' . $mimeTypes[$ext]);
    }
    
    readfile($frontendFile);
    return true;
}

http_response_code(404);
echo '404 Not Found';
return true;