# ADR-001 — Adoptar Spec Driven Design (SDD) como metodología de desarrollo

- **Estado:** Aceptado
- **Fecha:** 2026-05-22
- **Autores:** Equipo PDD Creator

---

## Contexto

El proyecto PDD Creator genera documentos PDD a partir de transcripciones usando IA. Está en etapa inicial y necesita una metodología que garantice que cada funcionalidad esté bien definida antes de implementarse, reduciendo retrabajo y malentendidos.

## Decisión

Adoptamos **Spec Driven Design (SDD)** como metodología de desarrollo, implementado sobre GitHub con tres artefactos:

1. **Issue Template (`spec.md`)** — toda nueva funcionalidad o cambio comienza como un Issue con una especificación estructurada (contexto, input/output, criterios de aceptación).
2. **PR Template** — cada Pull Request referencia obligatoriamente el Issue-spec aprobado y lista los criterios de aceptación cubiertos.
3. **ADRs en `docs/ADR/`** — las decisiones de arquitectura significativas se documentan aquí para dejar trazabilidad.

### Flujo de trabajo

```
Issue (spec) → review/aprobación → branch → código → PR → merge
```

Un PR sin Issue-spec aprobado no debe mergearse.

## Consecuencias

**Positivas:**
- Alineación del equipo antes de escribir código.
- Trazabilidad completa entre requerimiento y código.
- Onboarding más fácil: los Issues-spec documentan el "por qué" de cada feature.

**Negativas / trade-offs:**
- Agrega un paso de escritura antes de codear, lo cual puede sentirse lento en features pequeñas.
- Requiere disciplina del equipo para no saltarse el proceso.

## Alternativas consideradas

- **Solo comentarios en el código:** No da visibilidad antes de implementar ni trazabilidad a nivel de equipo.
- **Confluence / Notion:** Herramienta externa que desacopla la spec del ciclo de vida del código en GitHub.
