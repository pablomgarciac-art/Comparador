/* Cestuki: funciona sin conexión con la última copia de los precios */
var V = 'cestuki-v20';
var SHELL = ['./', 'index.html', 'productos.js', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png'];
self.addEventListener('install', function(e){
  e.waitUntil(caches.open(V).then(function(c){ return c.addAll(SHELL); }).then(function(){ return self.skipWaiting(); }));
});
self.addEventListener('activate', function(e){
  e.waitUntil(caches.keys().then(function(ks){ return Promise.all(ks.filter(function(k){ return k !== V; }).map(function(k){ return caches.delete(k); })); }).then(function(){ return self.clients.claim(); }));
});
self.addEventListener('fetch', function(e){
  var r = e.request;
  if(r.method !== 'GET') return;
  var u = new URL(r.url);
  if(u.origin !== location.origin) return;           /* mapas, fotos y APIs van directos a la red */
  /* primero la red (datos al día); si no hay conexión, la copia guardada */
  e.respondWith(fetch(r).then(function(res){
    var cp = res.clone(); caches.open(V).then(function(c){ c.put(r, cp); }); return res;
  }).catch(function(){ return caches.match(r).then(function(m){ return m || caches.match('index.html'); }); }));
});
