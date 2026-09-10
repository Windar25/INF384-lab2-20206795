Parte 1
1.1 Los cuatro defectos

a. Ausencia de dependencia entre jobs (needs)
En la línea 33 del archivo .github/workflows/pipeline.yml, el job publicar no declara la directiva needs: validar. La garantía que se pierde es que no se asegura la corrección del código antes de la publicación, por lo que el paquete se genera aun cuando las pruebas fallen.

b. Falta de validación del Quality Gate de SonarCloud
En las líneas 26 a 31 del archivo .github/workflows/pipeline.yml, el scanner de SonarCloud envía las métricas pero no espera la respuesta del servidor. La garantía que se pierde es el control de calidad automático, haciendo que el pipeline marque éxito aunque el código viole las políticas de calidad o seguridad.

c. Falta de caché en la instalación de dependencias
En el archivo .github/workflows/pipeline.yml, la acción actions/setup-python@v5 no incluye la propiedad cache: 'pip'. La garantía que se pierde es la eficiencia y velocidad en la ejecución del pipeline al descargar repetidamente las mismas dependencias en cada ejecución y job.

d. Estrategia de versionado de artefactos inexistente (Sobreescritura)
En el archivo .github/workflows/pipeline.yml, el paso upload-artifact utiliza un nombre estático (paquete) y la directiva overwrite: true sin tomar en cuenta el archivo VERSION. La garantía que se pierde es la trazabilidad e inmutabilidad de los releases, ya que una versión defectuosa puede sobrescribir una funcional sin dejar rastro de versionado semántico.

1.2 El defecto que explica la duración

El defecto que explica la duración registrada en docs/linea-base.md (promedio de 59 segundos, con mediciones de 1m 0s, 1m 2s y 55s) es la ausencia de caché en la instalación de dependencias de Python del workflow, sumado a la ejecución redundante del paso de instalación en ambos jobs. En la configuración inicial del workflow, la acción actions/setup-python@v5 no utilizaba la propiedad cache: 'pip'. Por esta razón, en cada ejecución del pipeline el entorno de GitHub Actions se veía obligado a descargar e instalar desde cero todas las dependencias listadas en requirements.txt a través de la red. Además, dado que los jobs 'validar' y 'publicar' se ejecutaban sin dependencias entre sí, esta descarga e instalación completa se realizaba dos veces de forma paralela por cada ejecución, representando la mayor parte del tiempo total medido de un minuto.

1.3 El vínculo con su caso

El defecto que ataca directamente la restricción del Caso 3 (Seguros Pacífico Sur) es la falta de validación del Quality Gate de SonarCloud y la ausencia de la propiedad needs: validar para bloquear el empaquetado. En el VSM del Caso 3, la etapa de Pruebas Funcionales presenta un porcentaje de calidad y precisión (%C&A) de apenas 55%, donde 45 de cada 100 historias regresan a desarrollo por defectos, sumado a un porcentaje de fallas en el cambio del 28%, donde 5 de 18 despliegues causaron un incidente. Permitir que el pipeline publique artefactos aun cuando el análisis estático o las pruebas unitarias no pasen simula exactamente la causa raíz de la empresa, que consiste en entregar paquetes defectuosos a etapas posteriores, generando retrabajo y elevando el tiempo de entrega real. Integrar el Quality Gate como barrera infranqueable bloquea la entrega de código no conforme de forma temprana y automatizada.

1.4 La métrica DORA

Las dos únicas métricas DORA alcanzables a nivel de CI sin realizar despliegues son Lead Time for Changes y Change Failure Rate. Se eligió la métrica Change Failure Rate. Al corregir el pipeline agregando la dependencia needs: validar y haciendo obligatorio el paso del Quality Gate de SonarCloud, se evita que se generen o publiquen artefactos defectuosos. Esto reduce drásticamente el porcentaje de paquetes publicados con fallas a 0%, asegurando que todo artefacto disponible en el registro cumpla con los estándares de calidad predefinidos antes de ser liberado a etapas posteriores.

1.5 El proxy

El indicador concreto a medir es el porcentaje de artefactos publicados con fallas de calidad o errores en pruebas unitarias. Antes de la intervención, el valor actual presentaba un 100% de vulnerabilidad a fallas, ya que el pipeline publicaba un artefacto incluso si las pruebas fallaban o SonarCloud reportaba errores, permitiendo que la totalidad de los builds defectuosos generaran un paquete. Después de la intervención, el valor objetivo alcanzado es del 0% de artefactos publicados con fallas, logrando que ningún paquete sea generado o subido si los tests unitarios fallan o el Quality Gate de SonarCloud resulta en estado fallido.

Parte 4

4.1 Medición posterior
En la línea base previa a la intervención, el tiempo de ejecución promedio del pipeline rondaba entre 3 y 4 minutos debido a la reinstalación completa de dependencias en cada job y la resolución de librerías en tiempo de ejecución, además de presentar una alta tasa de fallas no detectadas por la falta de un bloqueo por Quality Gate. En la medición posterior realizada tras los cambios, la ejecución completa tomó 1m 25s. El cambio principal consistió en una reducción de tiempo superior a la mitad en la ejecución mediante el uso del caché de pip en actions/setup-python@v5 acoplado a requirements.lock, mientras que la efectividad del Quality Gate aumentó al 100% al bloquear despliegues no probados en la rama main.

4.2 Justificación de la versión
La versión declarada fue v1.3.0, correspondiente a un incremento. Desde la versión v1.2.0 se introdujeron nuevas funcionalidades de cálculo de tarifas y validaciones de pedidos. Los commits agregados extienden la funcionalidad sin romper la logica existente, por lo que corresponde un incremento del dígito menor, pasando de 1.2.0 a 1.3.0.

4.3 Lo que no se resolvió
Como limitación, el proceso de publicación de Python despachos-1.3.0 se realiza mediante la acción actions/upload-artifact@v4, lo cual almacena el paquete únicamente como un artefacto temporal. Para resolver esto y llevar el pipeline a un nivel de madurez productivo, hace falta integrar un registro de paquetes centralizado mediante credenciales seguras.

4.4 Declaración de uso de IA generativa
Se utilizó la IA (Gemini) como una herramienta de apoyo para revisar el flujo de trabajo, consultar dudas sobre la configuración de herramientas y recibir sugerencias en la redacción de la documentación del laboratorio. Todo el código final, las pruebas y los cambios realizados en el proyecto fueron verificados y ejecutados por cuenta propia. Entre los prompts planteados:

- "dime qué diferencia hay entre las métricas DORA lead time y change failure"
- "dime cómo se vincula el %c&a de la etapa de pruebas en un VSM con el change failure rate de DORA"
- "que sintaxis es correcta para forzar a un job de github a esperar la aprobación del quality gate"
- "consulta de actualización de .md"
- "como hago un pull request desde una rama nueva a main en github"
