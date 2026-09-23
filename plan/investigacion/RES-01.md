# RES-01 · Persistencia de sesión en navegadores móviles y PWA

## Fuentes consultadas

- https://webkit.org/blog/9521/intelligent-tracking-prevention-2-3/ — Intelligent Tracking Prevention de WebKit / Safari
- https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/ — Ampliación de ITP: purga de datos locales tras inactividad
- https://developer.apple.com/forums/thread/710157 — Foro oficial Apple: datos locales en PWA en iOS
- https://www.netguru.com/blog/how-to-share-session-cookie-or-state-between-pwa-in-standalone-mode-and-safari-on-ios — Cookies en PWA entre navegador y standalone mode
- https://medium.com/@bloodturtle/why-your-cookies-disappear-on-mobile-chrome-after-restart-the-missing-secure-and-samesite-settings-76e0883f01eb — Persistencia de cookies en Chrome Android
- https://blog.google/products/chrome/privacy-sandbox-tracking-protection/ — Chrome Tracking Protection
- https://snowplow.io/blog/tracking-cookies-length — Restricciones de cookies por IP (Safari)
- https://learn.microsoft.com/en-nz/answers/questions/5850313/session-duration — Reauthenticación frecuente y fricción de usuario
- https://developer.apple.com/forums/thread/66566 — SFSafariViewController y cookies en background

## Hechos

- H1: Las cookies HTTP server-set con atributo `HttpOnly` en Safari iOS (first-party domain) persisten según su valor de expiración configurado (hasta ~400 días), sin limitación automática de 7 días. Fuente: https://webkit.org/blog/9521/intelligent-tracking-prevention-2-3/

- H2: Safari limita cookies creadas por JavaScript (client-side) a 7 días de duración, independientemente del valor de expiración configurado. Fuente: https://webkit.org/blog/9521/intelligent-tracking-prevention-2-3/

- H3: En iOS 13.4 y posteriores, Safari elimina datos locales (localStorage, IndexedDB, SessionStorage, Service Workers) después de 7 días de inactividad del usuario (sin interacción con el sitio). Sin embargo, las PWAs agregadas a la pantalla de inicio tienen su propio contador de días de uso y NO están sujetas a esta purga. Fuente: https://developer.apple.com/forums/thread/710157

- H4: En Android Chrome, las cookies solo persisten si tienen un valor explícito de `Expires` o `Max-Age`. Las cookies sin estas atributos se eliminan cuando el navegador se cierra. Fuente: https://medium.com/@bloodturtle/why-your-cookies-disappear-on-mobile-chrome-after-restart-the-missing-secure-and-samesite-settings-76e0883f01eb

- H5: Chrome no tiene un equivalente directo a ITP de Safari. Chrome implementa "Tracking Protection" que bloquea cookies de terceros gradualmente, pero no elimina cookies automáticamente tras un período de inactividad. Fuente: https://blog.google/products/chrome/privacy-sandbox-tracking-protection/

- H6: Safari 16.4+ añadió una restricción: las cookies HTTP de servidores behind third-party CNAMEs o third-party IP tienen límite de 7 días; las de servidores first-party IP persisten hasta ~400 días. Fuente: https://snowplow.io/blog/tracking-cookies-length

- H7: En Android y Desktop, un PWA instalado comparte la misma cookie store que el navegador desde el cual se instaló. Fuente: https://www.netguru.com/blog/how-to-share-session-cookie-or-state-between-pwa-in-standalone-mode-and-safari-on-ios

- H8: Reauthenticación frecuente causa "MFA fatigue" que aumenta la fricción de usuario y abre puerta a phishing. Las mejores prácticas recomiendan reauthenticación periódica (cada varias horas/días) en lugar de cada vez. Fuente: https://learn.microsoft.com/en-nz/answers/questions/5850313/session-duration

- H9: SFSafariViewController (en apps iOS) descarta cookies no-persistentes después de que la app va al background, aunque la cookie haya sido configurada como persistente en la respuesta HTTP. Fuente: https://developer.apple.com/forums/thread/66566

## Vacíos

- V1: No hay fuente pública clara que especifique diferencias de persistencia de cookies `HttpOnly` entre pestañas activas y pestañas en background en Safari iOS o Chrome Android. Las fuentes hablan de purgas generales tras inactividad sin distinguir si el usuario esté en una pestaña activa vs background.

- V2: No hay desglose detallado del mecanismo específico por el cual sesiones de larga duración crean fricción de UX (más allá de factores generales de seguridad como "MFA fatigue"). Las fuentes abordan el equilibrio seguridad-fricción y mejores prácticas, pero no el mecanismo preciso.
