# Resultado de Aprendizaje 3: Puesta en Producción Segura

**Alumno:** Ruben Ferrer
**Asignatura:** Puesta en Producción Segura (PPS)
**Curso:** 2025/2026

## Descripción General

Este repositorio documenta las actividades realizadas para el Resultado de Aprendizaje 3 (RA3), centrado en el endurecimiento (hardening) de servidores web, la contenerización de servicios y el análisis práctico de vulnerabilidades en aplicaciones web.

El proyecto se divide en bloques temáticos que abordan desde la configuración segura de servidores Apache y Nginx hasta la explotación ética de vulnerabilidades en entornos controlados.

## Estructura del Proyecto

A continuación se detalla el contenido de cada módulo:

### RA3_1: Hardening de Servidores Web
Este módulo es el núcleo de la práctica de defensa. Se implementa una arquitectura segura basada en contenedores Docker.
* **Tecnologías:** Docker, Apache, Nginx (Reverse Proxy), ModSecurity (WAF), OWASP CRS.
* **Objetivos:** Implementación de SSL/TLS, cabeceras de seguridad HTTP, mitigación de ataques DoS y configuración de reglas de firewall de aplicación web.
* **Ubicación:** [Ir a la documentación de RA3_1](./RA3_1/README.md)

### RA3_2: Análisis de Vulnerabilidades (DVWA)
Entorno de laboratorio para el estudio de vulnerabilidades web comunes (OWASP Top 10).
* **Tecnologías:** Damn Vulnerable Web Application (DVWA), Docker.
* **Alcance:** Documentación técnica de la explotación y mitigación de vulnerabilidades como SQL Injection, XSS, CSRF y fuerza bruta.
* **Ubicación:** [Ir a la documentación de RA3_2](./RA3_2/README.md)

---

## Requisitos Previos Generales

Para ejecutar los proyectos contenidos en este repositorio, se requiere:

* **Sistema Operativo:** Linux (Recomendado) o Windows con WSL2.
* **Motor de Contenedores:** Docker Engine y Docker Compose instalados.
* **Navegador Web:** Firefox (Recomendado para la manipulación de cabeceras y peticiones).
* **Herramientas de Red:** `curl`, `openssl`.

---

## Nota sobre la Metodología de Construcción (RA3_1)

Para el módulo RA3_1, se ha seguido una estrategia de **Layered Docker Builds** (Construcción por Capas). Se ha modificado el orden lógico sugerido en el enunciado original para garantizar la coherencia técnica, priorizando la generación de certificados SSL antes de la configuración de servicios que dependen de HTTPS (como HSTS).

Las imágenes base y finales se encuentran disponibles en DockerHub bajo el usuario `brean19`.
