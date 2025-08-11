self.addEventListener('install', function (event) {
  console.log('[ServiceWorker] Installed');
});

self.addEventListener('fetch', function (event) {
  // Optional caching logic
});
