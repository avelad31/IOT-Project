# Sistema de Seguridad por Reconocimiento Facial
El proyecto consiste en un sistema de seguridad basado en análisis biométrico facial, capaz de diferenciar personas en tiempo real mediante reconocimiento de patrones. El código personalizado permite la identificación de personas de una base de datos, la creación de una malla facial en tiempo real y el análisis de movimientos faciales, como el parpadeo. Usando el ESP32 y el protocolo Modbus, se activa un relé para abrir una chapa eléctrica si la persona es identificada.

## Flujo del Proyecto

1. Inicio de Reconocimiento Facial: El usuario ejecuta el código Python.
2. Encendido de Cámara: Se muestra la interfaz con la vista en tiempo real de la cámara.
3. Comparación de Rostros: El sistema compara el rostro capturado con los de la base de datos. Si la similitud es superior al 65%, se identifica al usuario; de lo contrario, se etiqueta como "Desconocido".
4. Base de Datos: Contiene imágenes de usuarios autorizados.
5. Detección de Parpadeos: Verifica el parpadeo del usuario para evitar fraudes.
6. Recepción de Señal: El ESP32 recibe una señal (1 para éxito, 0 para falla) después de la verificación.
7. Apertura de Chapa: El ESP32 activa el relé para abrir la chapa durante 3 segundos si la verificación es exitosa.
La configuración del ESP32 incluye:

- Iniciar Dispositivo: Alimentar el ESP32 con un cargador de 5V.
- Conectar a WiFi: Programar el ESP32 para conectarse a la red "UNI_Libre".
- Preparar Servidor Modbus: Configurar el ESP32 como servidor Modbus para recibir la señal del código Python.
El proceso se muestra en un diagrama de flujo y se detalla la configuración del ESP32 para complementar el código Python.
