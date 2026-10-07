# tomcat-monitor
Monitor apache tomcat 11.0.X version changes starting from a determinated package

### ¿Qué ocurrirá exactamente cuando se detecte un cambio?

Cuando aparezca una nueva versión de Tomcat 11.0.x (por ejemplo, al pasar de `11.0.1` a `11.0.2`) y existan diferencias en el paquete `java/org/apache/catalina/tribes`, la Action realizará automáticamente lo siguiente:

#### 1. Generación del informe (`diff_summary.txt`)

El script de Python comparará las dos últimas etiquetas (`tags`) publicadas en el repositorio oficial de Apache Tomcat. Si hay diferencias en `java/org/apache/catalina/tribes`:

* Establecerá la variable de salida `has_changes=true`.
* Generará un archivo de resumen `diff_summary.txt` con el diff exacto de Git formatado en Markdown (truncado a 3.500 caracteres si fuera muy extenso para evitar sobrepasar límites).

#### 2. Creación automática de un Issue en tu repositorio

La acción `peter-evans/create-issue-from-file@v5` se activará al detectar `has_changes == 'true'` y creará un nuevo **Issue** en tu repositorio de GitHub con la siguiente estructura:

* **Título:**
`🚨 Cambios en Tomcat Tribes 11 (11.0.x)` *(con la versión nueva detectada)*
* **Etiquetas (Labels):**
`tomcat-tribes`, `dependencies`
* **Cuerpo del Issue:**
Irá firmado con el resumen del código modificado, similar a esto:
> Se han detectado cambios en **org.apache.catalina.tribes** entre Tomcat `11.0.1` y `11.0.2`:
> ```diff
> --- a/java/org/apache/catalina/tribes/group/GroupChannel.java
> +++ b/java/org/apache/catalina/tribes/group/GroupChannel.java
> @@ -123,7 +123,7 @@
> - ... líneas eliminadas
> + ... líneas añadidas
> 
> ```
> 
> 



---

### ¿Y si NO hay cambios en esa versión?

Si sale una versión `11.0.x` pero las modificaciones de Tomcat corresponden a otros paquetes (como `catalina/connector`, `coyote`, etc.) y **no a Tribes**, el script asignará `has_changes=false`, la tarea finalizará correctamente en verde y **no creará ningún Issue innecesario**.