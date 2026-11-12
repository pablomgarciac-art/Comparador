# Cestuki

**Compra mejor. Paga menos.** · Compara · Ahorra · Disfruta

Comparador de precios de supermercados con foto. Abres la app, buscas un producto y ves el mismo producto en Mercadona, Lidl, Carrefour y Dia, ordenado por precio del envase (o por kilo / litro). Pensado primero para el móvil, instalable como app.

## Qué hace

- **Comparador de cestas** (Mi lista → Comparar): cuánto cuesta toda tu lista en cada súper, con equivalentes cuando falta un producto y botón para pasar la lista a ese súper.
- **Alternativas más baratas** en la ficha de cada producto.
- **Filtros de dieta** (sin gluten, sin lactosa, vegano, ecológico, integral, sin azúcar) deducidos del nombre del producto.
- **Enviar la lista por WhatsApp** con un toque.

- **Búsqueda** con atajos (leche, yogur, huevos…) y tus últimas búsquedas. Al abrir la app no hay ninguna búsqueda hecha.
- **Ficha de producto**: toca un producto y ves foto grande, precio, precio por kg/litro, formato y enlace a la tienda.
- **Mi lista de la compra**: añade productos con «+ Añadir», apunta cosas a mano, marca lo que ya has cogido (se tacha), cambia cantidades, añade notas, agrupa por súper y suma el total. Avisa si un precio ha subido o bajado, ofrece «Ver alternativas», permite deshacer, desmarcar todo para reutilizar y compartir la lista.
- **Favoritos** (♥): tus productos de siempre, para pasarlos a la lista con un toque.
- Todo se guarda en tu móvil. Funciona sin conexión.

## Datos

- Precios y fotos reales de Mercadona, Dia, Carrefour, Lidl y Alimerka (más de 5.000 productos) en `productos.js`, con la fecha de la copia. La app avisa si tienen 3 días o más.
- Son precios de la tienda online: pueden variar según tu tienda o código postal.
- Cobertura desigual: Carrefour y Dia traen solo parte de su catálogo.
- Las fotos se cargan desde las webs de cada cadena; si alguna las bloquea, la ficha muestra «Sin foto».
- Aldi, El Corte Inglés, Spar, Cash Fresh, Alcampo y Eroski no tienen precios todavía.

## Publicarlo con GitHub Pages

1. Repositorio **público** en GitHub.
2. Sube **todos los ficheros**: `index.html`, `productos.js`, `manifest.webmanifest`, `sw.js`, los cuatro `.png` de iconos y `README.md`.
3. **Settings → Pages** → *Deploy from a branch*, rama `main`, carpeta `/ (root)`.
4. En uno o dos minutos estará en `https://TU-USUARIO.github.io/NOMBRE-DEL-REPO/`.

## Instalar como app

Desde la dirección `https`: en Android, botón «Instalar la app» o menú del navegador → *Instalar aplicación*. En iPhone (Safari): Compartir → *Añadir a pantalla de inicio*. Se abre a pantalla completa, sin barra del navegador.

## Actualizar los precios

`productos.js` es una copia del 10 de noviembre de 2026. Para refrescarla hay que volver a ejecutar los lectores de precios del proyecto EasyCompra (se pueden programar a diario con GitHub Actions) y regenerar el fichero.

## Créditos y licencias

- Datos de precios y fotos: proyecto abierto [EasyCompra](https://github.com/elopositor/easycompra) (licencia MIT), que lee las webs de Mercadona, Dia, Carrefour, Lidl y Alimerka. Revisa los términos de uso de cada cadena antes de un uso comercial: las fotos y los datos son suyos.
- Logos: marcas de sus respectivas empresas, usadas solo para identificar cada cadena.
