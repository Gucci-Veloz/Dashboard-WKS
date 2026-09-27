# Vinculación de impresora HP Smart Tank 750 en red (Ubuntu 24.04)

**Contexto:** Impresora HP Smart Tank 750 series en red local de oficina, no detectada por descubrimiento automático (mDNS/SLP) en Ubuntu 24.04.3 LTS.

---

## 1. Localizar la impresora en la red

Escaneo general de la subred para listar hosts activos:

```bash
sudo apt install nmap -y
nmap -sn 192.168.1.0/24
```

Filtrado por puertos característicos de impresión (IPP y JetDirect) para reducir la lista de candidatos:

```bash
nmap -p 631,9100 --open 192.168.1.0/24
```

Resultado: IP identificada con ambos puertos abiertos → `192.168.1.176`

---

## 2. Confirmar la identidad del dispositivo

Verificación directa vía navegador, accediendo al servidor web embebido de la impresora:

```
http://192.168.1.176
```

Confirmado: página de bienvenida "HP Smart Tank 750 series — Embedded Web Server (Servidor Web integrado)".

---

## 3. Configurar la impresora en CUPS

Herramienta usada: `system-config-printer` (interfaz gráfica de CUPS).

Pasos:
1. **Impresoras → Añadir**
2. Dispositivo: **Protocolo de impresión en Internet (ipp)**
3. URI del dispositivo:
```
ipp://192.168.1.176/ipp/print
```
4. Conexión: **IPP (ipp)**
5. Siguiente → el sistema detectó el modelo automáticamente vía **IPP Everywhere** (driver genérico universal, sin necesidad de HPLIP ni driver específico de HP)
6. Nombre de impresora: `HP-Smart-Tank-750`
7. Descripción: `HP Smart Tank 750`
8. **Aplicar**

---

## Resultado

Impresora vinculada y operativa en el sistema mediante IPP, sin dependencia de drivers propietarios HP.

| Parámetro | Valor |
|---|---|
| IP | 192.168.1.176 |
| Protocolo | IPP |
| URI | `ipp://192.168.1.176/ipp/print` |
| Driver | IPP Everywhere (autodetectado) |
| Nombre en sistema | HP-Smart-Tank-750 |

---

## Información adicional a solicitar al dueño para que un Agente de IA pueda imprimir

Lo anterior cubre la vinculación manual ya realizada. Para que un Agente de IA pueda mandar imprimir de forma autónoma, falta definir y solicitar lo siguiente:

**1. Dónde va a vivir el Agente de IA (lo más importante, define todo lo demás)**
- Si el agente corre en **el mismo equipo/red de oficina** (mismo Ubuntu o cualquier máquina en esa LAN): con lo ya documentado alcanza — el agente solo necesita ejecutar `lp`/`lpr` o hablar con CUPS, apuntando a la cola ya configurada o directo a la URI IPP.
- Si el agente corre **fuera de esa red** (cloud, otro sitio, otro país): se necesita una forma de llegar a esa LAN — VPN, port-forward del router hacia 631/9100, o un servidor relay que reciba trabajos y los reenvíe al CUPS local. Sin esto, el agente remoto no puede tocar la impresora aunque sepa la IP.

**2. IP fija o reservación DHCP**
La IP `192.168.1.176` fue detectada por escaneo, no se confirmó si es estática. Pedirle al dueño que la impresora tenga **IP reservada en el router/DHCP** — si cambia, el agente deja de encontrarla.

**3. Confirmar si el servidor web embebido (Embedded Web Server) tiene contraseña de administrador**
Para imprimir normalmente no se necesita, pero si el agente algún día necesita consultar estado (niveles de tinta, atascos, cola) vía esa interfaz web o API, preguntar si hay usuario/contraseña de admin configurado.

**4. Qué máquina va a mantener la cola CUPS activa y encendida**
La cola se configuró en un equipo personal. Si el agente depende de esa cola (en vez de hablar IPP directo), esa máquina debe estar **siempre encendida y accesible** cuando el agente quiera imprimir. Preguntar al dueño si hay un equipo dedicado para esto (ej. un mini PC o servidor de oficina) en vez de depender de una laptop personal.

**5. Reglas de firewall/red internas**
Confirmar que no hay reglas que bloqueen tráfico entre el host del agente y los puertos 631 (IPP) / 9100 (JetDirect) — sobre todo si la oficina tiene VLANs separadas para impresoras.

**6. Formatos de archivo que la impresora acepta bien**
IPP Everywhere normalmente soporta PDF y PWG-Raster de forma nativa. Si el agente va a generar Word/Excel directamente, probablemente se necesite convertir a PDF antes de enviar — no es info que pedirle al dueño, pero es una decisión de diseño del agente que vale la pena anotar.
