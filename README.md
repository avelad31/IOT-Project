# Sistema de Seguridad por Reconocimiento Facial
El proyecto consiste en un sistema de seguridad por análisis biométrico facial, cuyo algoritmo logra diferenciar entre personas en tiempo real mediante reconocimiento de patrones. Además, se personaliza el código para el uso de funcionalidades que nos serán útiles como: identificación de personas de una determinada base de datos, creación de una malla facial en tiempo real y análisis de movimientos en el rostro durante un parpadeo. Usamos lo anterior para establecer la recepción de una señal con ESP32 vía WIFI con el protocolo de comunicación abierta Modbus, y así activar un relé que estará conectado a una chapa eléctrica si en caso la persona ha sido identificada en la base de datos.

## Flujo del Proyecto

1. Inicio de Reconocimiento Facial: El usuario ejecuta manualmente el código Python en un ordenador.
2. Encendido de Cámara: De forma automática se abrirá la interfaz de usuario donde se mostrará lo que registra la cámara en tiempo real.
3. Comparación de Rostros: El sistema compara el rostro capturado con los de la base de datos. Si la similitud es superior al 65%, se identifica al usuario; de lo contrario, se etiqueta como "Desconocido" y no permitirá al usuario avanzar al siguiente paso.
4. Database: Carpeta que contiene las imágenes .jpg o .png de los rostros de usuarios autorizados para el ingreso .
5. Detección de Parpadeos: Posterior a la función de Comparar Rostros, y ser identificado el usuario como un usuario autorizado, se habilitará la función de Detectar Parpadeos que, a través del uso de una malla facial, detectará el movimiento en el rostro del usuario autorizado al parpadear, esto es para evitar fraudes por parte de usuarios desconocidos con la fotografía de algún usuario registrado.
6. Recepción de Señal: El microcontrolador ESP32 será el encargado de recibir la señal que el código Python le envíe luego de haberle aplicado al usuario las funciones Comprar rostros y Detectar parpadeos, siendo que tras una verificación exitosa lo enviado sea una señal 1; y tras una verificación fallida, una señal 0..
7. Apertura de Chapa: El ESP32 activa el relé para abrir la chapa durante 3 segundos si la verificación es exitosa.
   
### La secuencia entre el ESP32 con el código en Python

- Iniciar Dispositivo: Alimentar el ESP32 con un cargador de 5V.
- Conectar a WiFi: Se configura el microcontrolador ESP32 programándolo con un código que lo conecte a la red Wifi “UNI_Libre”, se ingresa el nombre de la red y la contraseña en el código del microcontrolador. 
- Preparar Servidor Modbus: Se establece una conexión vía wifi entre el ESP32 y el código Python a través de su conexión a la misma red Wifi, y se configura el microcontrolador como servidor Modbus para que reciba la señal digital (1 o 0) del código Python.
  
El proceso se muestra en un diagrama de flujo y se detalla la configuración del ESP32 para complementar el código Python.



https://github.com/avelad31/IOT-Project/blob/main/Images/Circuito.png
#### WorkFlow del Sistema:
![Workflow System](https://github.com/avelad31/IOT-Project/blob/main/Images/Diagrama%20de%20flujo%20del%20sistema%20integral.png)

#### Circuito del Sistema:
![Circuit System](https://github.com/avelad31/IOT-Project/blob/main/Images/Circuito.png)


