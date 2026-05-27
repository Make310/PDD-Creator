Muestra todas las specs aprobadas y listas para implementar.

Ejecuta: `gh issue list --label "spec-approved" --state open`

Con el resultado:
1. Presenta una tabla con: número, título, asignado y fecha de creación.
2. Indica el total de specs pendientes.
3. Si hay más de una, sugiere empezar por la más antigua.
4. Recuerda que para cargar el contexto completo de una spec se usa `/spec <número>`.
