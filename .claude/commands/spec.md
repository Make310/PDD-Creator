Lee el Issue de GitHub con número $ARGUMENTS y úsalo como contexto de trabajo.

Ejecuta en secuencia:
- `gh issue view $ARGUMENTS`
- `gh issue view $ARGUMENTS --comments`

Presenta la información con esta estructura:

## Resumen
Número, título, estado, asignado, labels.

## Verificación
Confirma que tiene el label `spec-approved`. Si no lo tiene, advierte que la spec no está aprobada: se puede continuar leyendo o discutiendo la spec, pero no implementar.

## Contexto y objetivo
Problema que resuelve y objetivo en una oración.

## Comportamiento esperado
- **Input:** qué recibe el sistema (tipo, formato, ejemplo)
- **Output:** qué produce (tipo, formato, ejemplo)
- **Flujo principal:** pasos numerados

## Criterios de aceptación
Lista completa con checkboxes. Si alguno está en duda, señálalo.

## Casos límite y errores
Lista completa de escenarios edge.

## Preguntas abiertas
Si quedan preguntas sin responder, advierte que deben resolverse antes de codear.

## Notas de diseño
Restricciones técnicas, dependencias y decisiones relevantes.

## Comentarios del Issue
Muestra los comentarios con decisiones o aclaraciones importantes tomadas durante el review de la spec.

---
Al finalizar indica que estás listo para implementar y espera instrucciones.
