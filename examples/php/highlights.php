<?php
// Goal clips of one team as HTML you can drop into a page.
//
// Usage:
//   export GOALISE_TOKEN=your_api_token
//   php highlights.php 404        # 404 = Cagliari
//
// Needs PHP 7.4+ with allow_url_fopen enabled and nothing else.

$teamId = $argv[1] ?? 404;
$query = http_build_query(['team_id' => $teamId, 'category' => 'goal-clip']);

$context = stream_context_create(['http' => [
    'header' => "Authorization: Bearer " . getenv('GOALISE_TOKEN') . "\r\nAccept: application/json",
    'ignore_errors' => true, // read the JSON body of 4xx answers too
    'timeout' => 20,
]]);
$body = file_get_contents("https://api.goalise.com/api/v3/highlights?$query", false, $context);
$data = json_decode((string) $body, true);

if (($data['status'] ?? null) !== 'success') {
    $codes = array_column($data['errors'] ?? [], 'code');
    fwrite(fopen('php://stderr', 'w'), 'API error: ' . ($codes ? implode(', ', $codes) : 'no answer') . PHP_EOL);
    exit(1);
}

foreach ($data['response'] as $clip) {
    $title = htmlspecialchars($clip['title'] ?? 'Goal clip');
    // Embed only what the rights holder allows; otherwise link to the watch page.
    if ($clip['restriction']['embeddable'] === true && $clip['embed_url']) {
        printf(
            '<iframe src="%s" title="%s" allowfullscreen loading="lazy"></iframe>' . PHP_EOL,
            htmlspecialchars($clip['embed_url']),
            $title
        );
    } elseif ($clip['url']) {
        printf('<a href="%s">%s</a>' . PHP_EOL, htmlspecialchars($clip['url']), $title);
    }
}
