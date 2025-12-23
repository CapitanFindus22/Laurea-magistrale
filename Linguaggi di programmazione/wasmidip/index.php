<?php
// Cacheless server
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
include "web_page/player.html";
?>
