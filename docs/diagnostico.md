1.1 Los cuatro defectos


a. **Ausencia de dependencia entre jobs (`needs`)**
   * **Archivo y líneas:** `.github/workflows/pipeline.yml` (Línea 33)
   * **Qué está mal:** El job `publicar` no declara `needs: validar`.
   * **Garantía que se pierde:** No se garantiza que el código sea correcto antes de publicar. El paquete se genera aunque las pruebas fallen.

b. **Falta de validación del Quality Gate de SonarCloud**
   * **Archivo y líneas:** `.github/workflows/pipeline.yml` (Líneas 26-31)
   * **Qué está mal:** El scanner de SonarCloud envía las métricas pero no espera la respuesta del servidor (`sonar.qualitygate.wait=true`).
   * **Garantía que se pierde:** Se pierde el control de calidad automático. El pipeline marca "éxito" aunque el código viole las políticas de calidad o seguridad.

c. **Falta de caché en la instalación de dependencias**
   * **Archivo y líneas:** `.github/workflows/pipeline.yml` (Líneas 16-17 y 42-43)
   * **Qué está mal:** La acción `actions/setup-python@v5` no incluye la propiedad `cache: 'pip'`.
   * **Garantía que se pierde:** Se pierden eficiencia y velocidad en el pipeline al descargar repetidamente las mismas dependencias en cada ejecución y job.

d. **Estrategia de versionado de artefactos inexistente (Sobreescritura)**
   * **Archivo y líneas:** `.github/workflows/pipeline.yml` (Líneas 50-55)
   * **Qué está mal:** El paso `upload-artifact` usa un nombre estático (`paquete`) y `overwrite: true` sin tomar en cuenta el archivo `VERSION`.
   * **Garantía que se pierde:** Se pierde la trazabilidad e inmutabilidad de los releases. Una versión defectuosa puede sobrescribir una funcional sin dejar rastro de versionado semántico.




## 1.2 El defecto que explica la duración

El defecto que explica la duración registrada en `docs/linea-base.md` (promedio de **59 segundos**, con mediciones de **1m 0s**, **1m 2s** y **55s**) es la **ausencia de caché en la instalación de dependencias de Python** (Líneas 16-17 y 42-43 del workflow), sumado a la ejecución redundante del paso de instalación en ambos jobs.

**Sustento:**
En la configuración actual del workflow, la acción `actions/setup-python@v5` no utiliza la propiedad `cache: 'pip'`. Por esta razón, en cada ejecución del pipeline el entorno de GitHub Actions se ve obligado a descargar e instalar desde cero todas las dependencias listadas en `requirements.txt` a través de la red. Además, dado que los jobs `validar` y `publicar` se ejecutan sin dependencias entre sí, esta descarga e instalación completa se realiza **dos veces de forma paralela por cada ejecución**, representando la mayor parte del tiempo total medido (1 minuto).


## 1.3 El vínculo con su caso

El defecto que ataca directamente la restricción del **Caso 3 (Seguros Pacífico Sur)** es la **falta de validación del Quality Gate de SonarCloud** (y la ausencia de la propiedad `needs: validar` para bloquear el empaquetado).

**Sustento y cita del VSM:**
En el VSM del Caso 3, la etapa de **Pruebas Funcionales** presenta un **%C&A de apenas 55%** (donde 45 de cada 100 historias regresan a desarrollo por defectos), sumado a un **Porcentaje de fallas en el cambio del 28%** (5 de 18 despliegues causaron un incidente). 

Permitir que el pipeline publique artefactos aun cuando el análisis estático o las pruebas unitarias no pasen simula exactamente la causa raíz de la empresa: **entregar paquetes defectuosos a etapas posteriores, generando retrabajo y elevando el tiempo de entrega real**. Integrar el Quality Gate como barrera infranqueable bloquea la entrega de código no conforme de forma temprana y automatizada.



## 1.4 La métrica DORA

Las dos únicas métricas DORA alcanzables a nivel de CI (sin realizar despliegue a entornos de producción) son **Lead Time for Changes** y **Change Failure Rate**.

**Métrica elegida:** **Change Failure Rate (Porcentaje de fallas en los cambios)**

**Justificación:**
Al corregir el pipeline agregando la dependencia `needs: validar` y haciendo obligatorio el paso del Quality Gate de SonarCloud, evitamos que se generen o publiquen artefactos defectuosos. Esto reducirá drásticamente el porcentaje de paquetes publicados con fallas a **0%**, asegurando que todo artefacto disponible en el registro cumpla con los estándares de calidad predefinidos antes de ser liberado a etapas posteriores.




## 1.5 El proxy

**Indicador concreto a medir:** 
Porcentaje de artefactos publicados con fallas de calidad o errores en pruebas unitarias.

* **Valor actual (Antes de la intervención):** **100% de vulnerabilidad a fallas.** El pipeline publica un artefacto incluso si las pruebas fallan o SonarCloud reporta errores, permitiendo que el 100% de los builds defectuosos generen un paquete.
* **Valor objetivo (Después de la intervención):** **0% de artefactos publicados con fallas.** Ningún paquete será generado o subido si los tests unitarios fallan o el Quality Gate de SonarCloud resulta en estado *FAILED*.
