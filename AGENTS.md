# AGENTS.md — Mapa de navegación

Punto de entrada para cualquier agente. Lee esto primero, luego solo lo que necesites.

## Convención de nombres

Los features de este proyecto son Issues de GitHub. Usa siempre `issue_<n>` como identificador:

- `progress/impl_issue_2.md` — implementación del Issue #2
- `progress/review_issue_2.md` — revisión del Issue #2
- `feat/issue-2` — rama de desarrollo del Issue #2

## Conventional Commits

Formato obligatorio para todos los commits: `type(issue-<n>): descripción en imperativo`

| Type | Cuándo usarlo |
|------|--------------|
| `feat` | nueva funcionalidad |
| `fix` | corrección de bug |
| `refactor` | restructuración sin cambio de comportamiento |
| `test` | agregar o corregir tests |
| `docs` | solo documentación |
| `chore` | configuración, dependencias, archivos de proyecto |

Ejemplos:
- `feat(issue-2): add PDF export endpoint`
- `fix(issue-2): handle null response in parser`
- `test(issue-2): add edge cases for empty input`


## Mapa del repositorio

| Ruta | Qué contiene | Quién la usa |
|------|-------------|--------------|
| `AGENTS.md` | Este mapa | Todos, primero |
| `CLAUDE.md` | Rol e instrucciones del leader | Claude al arrancar sesión |
| `progress/current.md` | Estado de la sesión activa | Leader (escribe), todos (leen) |
| `progress/history.md` | Bitácora de sesiones pasadas | Leader (append al cerrar) |
| `progress/impl_issue_<n>.md` | Qué implementó el implementer | Reviewer (lee), leader (referencia) |
| `progress/review_issue_<n>.md` | Veredicto del reviewer | Leader (decide PR o retry) |
| `progress/feedback_issue_<n>.md` | Feedback del usuario/PR denegado | Leader (escribe), implementer (lee) |
| `.claude/agents/leader.md` | Rol del orquestador | Leader |
| `.claude/agents/implementer.md` | Rol del implementer | Implementer |
| `.claude/agents/reviewer.md` | Rol del reviewer | Reviewer |
| `.github/PULL_REQUEST_TEMPLATE.md` | Secciones del PR | Leader al crear PR |


## Reglas no negociables

1. **Un Issue a la vez** — no empezar el siguiente hasta cerrar el actual
2. **spec-approved obligatorio** — sin ese label no se codea
3. **Verificación antes de PR** — si hay suite de tests, deben pasar antes de crear el PR
4. **Subagentes escriben en disco** — no devuelven código al chat
5. **progress/ es la memoria** — todo lo que deba sobrevivir al context window va ahí
6. **Solo el leader escribe current.md** — implementer y reviewer no lo tocan
7. **El usuario tiene la última palabra** — si deniega el PR, se trata como `CHANGES_REQUESTED` aunque el reviewer haya aprobado

## Comandos útiles

```bash
# Ver specs pendientes
gh issue list --label "spec-approved" --state open

# Ver Issue completo con comentarios
gh issue view <n> --comments

# Cerrar Issue tras merge
gh issue close <n> --comment "Implementado en PR #<pr>"
```

