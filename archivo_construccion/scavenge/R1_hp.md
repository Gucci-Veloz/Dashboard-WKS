# R1 · HP Smart Tank 750: formatos y flujos

## Fuentes consultadas
- Local: `vinculacion-hp-smart-tank-750-ubuntu.md` (documento de vinculación manual de la impresora en Ubuntu 24.04)
- https://www.hp.com/emea_africa-en/products/printers/product-details/product-specifications/2100178990 (especificaciones oficiales HP)
- https://h20195.www2.hp.com/v2/GetPDF.aspx/c07767566.pdf (data sheet oficial HP, no se pudo procesar el contenido — ver Vacíos)
- https://support.hp.com/us-en/product/details/hp-smart-tank-750-series/2100043635 (portal de soporte HP, no se pudo cargar — ver Vacíos)
- https://sourceforge.net/p/hplip/news/2021/09/hplip-3218-release-notes/ (notas de versión HPLIP 3.21.8)
- https://developers.hp.com/hp-linux-imaging-and-printing/supported_devices/index (índice oficial de dispositivos soportados por HPLIP, no se pudo cargar — ver Vacíos)
- Búsquedas web generales sobre OpenPrinting/IPP Everywhere y el modelo Smart Tank 750 (sin entrada específica confirmada — ver Vacíos)

## Hechos
- H1: El lenguaje de impresión nativo documentado por HP es **HP PCL 3 GUI**. Fuente: hp.com/emea_africa-en, especificaciones del producto.
- H2: La impresora es compatible con **Apple AirPrint**, **Mopria Print Service** (certificado), **HP Print Service Plugin** (impresión desde Android), **HP Smart app** y **Wi-Fi Direct Printing**. Fuente: hp.com/emea_africa-en, especificaciones del producto.
- H3: Soporta **impresión dúplex automática** (dos caras). Fuente: hp.com/emea_africa-en, especificaciones del producto.
- H4: Tamaños de papel soportados: A4, A5, A6, B5 (JIS), sobres (DL, C5, C6, Chou #3, Chou #4), tarjetas (Hagaki, Ofuku Hagaki), y tamaños personalizados de 88.9 x 127 mm a 215.9 x 355.6 mm. Fuente: hp.com/emea_africa-en, especificaciones del producto.
- H5: Soporta impresión a **color y monocromo**, hasta 15 ppm en negro y 9 ppm en color (ISO). Fuente: hp.com/emea_africa-en, especificaciones del producto.
- H6: Conectividad: USB 2.0 de alta velocidad, Wi-Fi (2.4/5G dual band), Wi-Fi Direct, LAN, y Bluetooth low energy (mencionado en otras fichas técnicas, ver H9). Fuente: hp.com/emea_africa-en, especificaciones del producto.
- H7: La memoria del dispositivo es fija en **256 MB**, no ampliable. Fuente: hp.com/emea_africa-en, especificaciones del producto.
- H8: **HPLIP 3.21.8** (septiembre 2021) agregó soporte para modelos de la serie Smart Tank, incluyendo referencias a Smart Tank 750 en las notas de la versión. Fuente: sourceforge.net/p/hplip/news/2021/09/hplip-3218-release-notes/.
- H9: Resolución de impresión: hasta 1200 x 1200 dpi renderizados en negro, hasta 4800 x 1200 dpi optimizados en color. Fuente: búsqueda web con snippets de fichas técnicas de distribuidores (jarcomputers.com, tmt.my) que replican datos de la hoja de especificaciones oficial de HP — no verificado directamente contra el PDF oficial de HP (ver Vacíos).
- H10: El documento local confirma en la práctica que la vinculación en Ubuntu 24.04 se logró vía **IPP** (`ipp://<ip>/ipp/print`), con el driver detectado automáticamente como **IPP Everywhere** — sin necesidad de HPLIP ni driver propietario HP. Fuente: archivo local `vinculacion-hp-smart-tank-750-ubuntu.md`, secciones 3 y "Resultado".

## Contradicciones
- Ninguna detectada entre el documento local y las fuentes web consultadas. El documento local afirma que la impresora fue detectada vía IPP Everywhere en CUPS sin necesidad de HPLIP; esto es consistente con el hecho de que HP declara Mopria y AirPrint (ambos estándares construidos sobre IPP) como protocolos soportados, aunque ninguna fuente web pública consultada confirma explícitamente el término "IPP Everywhere" para este modelo (ver Vacíos V1).

## Vacíos
- V1: No se pudo confirmar en una fuente oficial de HP o de IPP Everywhere/Mopria.org que el Smart Tank 750 esté listado formalmente como certificado "IPP Everywhere". La evidencia de esto proviene únicamente del documento local (detección automática en CUPS), no de una fuente pública verificable.
- V2: No se pudo leer el contenido del data sheet oficial en PDF (h20195.www2.hp.com/v2/GetPDF.aspx/c07767566.pdf) — la herramienta de lectura no pudo procesar el binario. No se confirmaron directamente desde el PDF oficial: formatos nativos exactos aceptados por el motor de impresión (p. ej. si acepta PDF y/o PWG-Raster/URF de forma nativa vía IPP), ni el detalle completo de "HP PCL 3 GUI" como único lenguaje soportado.
- V3: No se pudo cargar la página de soporte oficial de HP (support.hp.com) por timeout, ni el índice oficial de dispositivos soportados de HPLIP (developers.hp.com) por error 403. No se confirmó directamente en fuente oficial de HP el nivel exacto de soporte HPLIP (hpcups, hpaio, fax) para este modelo específico, más allá de la mención en las notas de versión de HPLIP 3.21.8.
- V4: No se encontró una entrada específica y verificable del Smart Tank 750 en la base de datos pública de OpenPrinting (openprinting.org) que confirme su clasificación como impresora "driverless".
- V5: No se pudo verificar si la impresora acepta JPEG directamente vía IPP (formato común en impresión driverless) — ninguna fuente consultada lo menciona explícitamente para este modelo.
- V6: No se pudo confirmar si hay contraseña de administrador configurada por defecto en el servidor web embebido (Embedded Web Server), ni límites documentados de la interfaz IPP/API para consulta de estado (niveles de tinta, atascos, cola) — esto requiere acceso directo al dispositivo, fuera del alcance permitido para esta investigación.
