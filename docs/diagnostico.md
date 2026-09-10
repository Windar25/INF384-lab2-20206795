1. **Ausencia de dependencia entre jobs (`needs`)**
   * **Archivo y líneas:** `.github/workflows/pipeline.yml` (Línea 33)
   * **Qué está mal:** El job `publicar` no declara `needs: validar`.
   * **Garantía que se pierde:** No se garantiza que el código sea correcto antes de publicar. El paquete se genera aunque las pruebas fallen.

2. **Falta de validación del Quality Gate de SonarCloud**
   * **Archivo y líneas:** `.github/workflows/pipeline.yml` (Líneas 26-31)
   * **Qué está mal:** El scanner de SonarCloud envía las métricas pero no espera la respuesta del servidor (`sonar.qualitygate.wait=true`).
   * **Garantía que se pierde:** Se pierde el control de calidad automático. El pipeline marca "éxito" aunque el código viole las políticas de calidad o seguridad.

3. **Falta de caché en la instalación de dependencias**
   * **Archivo y líneas:** `.github/workflows/pipeline.yml` (Líneas 16-17 y 42-43)
   * **Qué está mal:** La acción `actions/setup-python@v5` no incluye la propiedad `cache: 'pip'`.
   * **Garantía que se pierde:** Se pierden eficiencia y velocidad en el pipeline al descargar repetidamente las mismas dependencias en cada ejecución y job.

4. **Estrategia de versionado de artefactos inexistente (Sobreescritura)**
   * **Archivo y líneas:** `.github/workflows/pipeline.yml` (Líneas 50-55)
   * **Qué está mal:** El paso `upload-artifact` usa un nombre estático (`paquete`) y `overwrite: true` sin tomar en cuenta el archivo `VERSION`.
   * **Garantía que se pierde:** Se pierde la trazabilidad e inmutabilidad de los releases. Una versión defectuosa puede sobrescribir una funcional sin dejar rastro de versionado semántico.
