# Cestuki

**Compra mejor. Paga menos.** · Compara · Ahorra · Disfruta

Comparador de precios de supermercados con foto. Portada → código postal (o ubicación) → te enseña los súpers que tienes cerca (OpenStreetMap) y compara el mismo producto entre cadenas. Pensado primero para el móvil. Por defecto ordena por precio del envase; también se puede ordenar por precio por kilo o litro.

## Estado

- **Precios y fotos reales** de Mercadona, Dia, Carrefour y Lidl (más de 5.000 productos), guardados en `productos.js` con la fecha de la copia. La página avisa si los datos tienen 3 días o más.
- **Aldi, El Corte Inglés, Spar, Cash Fresh, Alcampo y Eroski**: salen en el mapa y en el aviso de zona, pero todavía sin precios (no hay datos abiertos fiables).
- Los precios son los de la tienda online. Pueden variar según tu tienda o código postal.
- Cobertura desigual: Carrefour y Dia traen solo parte de su catálogo (por ejemplo, sin aceites de cocina en esta copia).
- Las fotos se cargan directamente desde las webs de cada cadena. Si una cadena las bloquea, la ficha muestra «Sin foto».

## Publicarlo con GitHub Pages

1. Crea un repositorio **público** en GitHub.
2. Sube **todos los ficheros juntos**: `index.html`, `productos.js`, `manifest.webmanifest`, `sw.js`, los cuatro `.png` de iconos y `README.md`.
3. En **Settings → Pages** elige *Deploy from a branch*, rama `main`, carpeta `/ (root)`.
4. En uno o dos minutos estará en `https://TU-USUARIO.github.io/NOMBRE-DEL-REPO/`.

Ábrela desde esa dirección `https`: con doble clic en el fichero el mapa de OpenStreetMap no carga (los precios y las fotos sí).

## Actualizar los precios

`productos.js` es una copia del 10 de noviembre de 2026. Para refrescarla hay que volver a ejecutar los lectores de precios del proyecto EasyCompra (se pueden programar a diario con GitHub Actions) y regenerar el fichero.

## Créditos y licencias

- Datos de precios y fotos: proyecto abierto [EasyCompra](https://github.com/elopositor/easycompra) (licencia MIT), que lee las webs de Mercadona, Dia, Carrefour y Lidl. Revisa los términos de uso de cada cadena antes de un uso comercial: las fotos y los datos son suyos.
- Mapa y tiendas: © colaboradores de [OpenStreetMap](https://www.openstreetmap.org/copyright), licencia ODbL.
- Logos: marcas de sus respectivas empresas, usadas solo para identificar cada cadena.

## Instalar como app

Abierta desde `https`, se puede instalar en el móvil y se abre a pantalla completa, sin barra del navegador. En Android: botón «Instalar la app» de la portada o menú del navegador → *Instalar aplicación*. En iPhone (Safari): Compartir → *Añadir a pantalla de inicio*. Guarda una copia para usarla sin conexión.
