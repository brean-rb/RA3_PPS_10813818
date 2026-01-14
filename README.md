# RA3 - Puesta en Producción Segura (Hardening)

**Alumno:** Ruben Ferrer
**Asignatura:** PPS
**Curso:** 2025/2026

Este repositorio contiene las prácticas correspondientes al Resultado de Aprendizaje 3 (RA3), enfocadas en el endurecimiento de servidores web y análisis de vulnerabilidades.

## Estructura del Repositorio

* **[RA3_1 - Apache & Nginx Hardening](./RA3/RA3_1/README.md):** Contenerización segura de servidores web implementando SSL, WAF (ModSecurity), Reglas OWASP y protección Anti-DoS.
* **RA3_2:** (Pendiente de realización)
* **RA3_3:** (Pendiente de realización)
* **RA3_4:** (Pendiente de realización)

## ⚠️ Nota Técnica sobre RA3_1

Para la realización del RA3_1, se ha optado por una **Estrategia de Construcción en Cascada (Layered Docker Builds)**. 

Se ha modificado el orden lógico sugerido en el enunciado para garantizar la coherencia técnica:
1. **Prioridad SSL:** Se ha integrado la Práctica 3.2 (Certificados) en la **Fase 1**.
2. **Justificación:** La implementación de **HSTS** (requerida en el hardening básico) exige una conexión HTTPS funcional. Sin certificados previos, no es posible aplicar políticas de transporte estricto.

Todas las imágenes Docker generadas son públicas y accesibles en DockerHub bajo el usuario: `brean19`.
