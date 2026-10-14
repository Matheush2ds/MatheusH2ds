<img width="100%" alt="Matheus Henrique: Software Engineer, Systems Analyst & Technical Project Manager" src="./assets/header-en.svg">

<div align="center">
  <br>
  <a href="https://optimasistemas.com"><kbd>&nbsp;&nbsp;optimasistemas.com&nbsp;&nbsp;</kbd></a>
  &nbsp;&nbsp;
  <a href="https://www.linkedin.com/in/matheus-henriquedev/"><kbd>&nbsp;&nbsp;LinkedIn&nbsp;&nbsp;</kbd></a>
  &nbsp;&nbsp;
  <a href="mailto:matheushenriqueds1223@gmail.com"><kbd>&nbsp;&nbsp;matheushenriqueds1223@gmail.com&nbsp;&nbsp;</kbd></a>
  &nbsp;&nbsp;
  <a href="./README.md"><kbd>&nbsp;&nbsp;Português (BR)&nbsp;&nbsp;</kbd></a>
</div>

<br>

## About

Software engineer, systems analyst, and founder at **Optima Sistemas**, where I design, architect, and operate B2B SaaS products and operational management platforms for service-oriented businesses. My work spans the full software lifecycle, from **systems analysis and project management** (requirements discovery, business process mapping, technical feasibility, and delivery coordination) to backend engineering and production operations. I focus on relational data modeling, complex domain rules, multi-tenant data isolation, and reliable integrations across business systems.

<table width="100%">
  <tr>
    <td width="25%" valign="top">
      <sub><b>OPERATION</b></sub><br>
      <code>Founder @ Optima Sistemas</code>
    </td>
    <td width="25%" valign="top">
      <sub><b>UNDERGRADUATE</b></sub><br>
      <code>B.S. in Computer Science</code>
    </td>
    <td width="25%" valign="top">
      <sub><b>POSTGRADUATE</b></sub><br>
      <code>Software Architecture & AI</code>
    </td>
    <td width="25%" valign="top">
      <sub><b>CORE FOCUS</b></sub><br>
      <code>Backend, Data & Systems Delivery</code>
    </td>
  </tr>
</table>

<br>

## Production Systems & Architecture

Proprietary commercial systems designed, built, and maintained in production at **Optima Sistemas**. Because these are commercial B2B products, their source repositories remain private; the architectural topology, domain boundaries, and engineering trade-offs behind each platform are detailed below:

<img width="100%" alt="Production Systems Architecture: Optima Control, Portal SST, and ERP de Temporada" src="./assets/architecture-en.svg">

<table width="100%">
  <tr>
    <td width="33.3%" valign="top">
      <b>Optima Control</b> &nbsp;<code>B2B SaaS</code><br><br>
      <sub>Operational and financial management platform built for pest control and environmental health companies.</sub><br><br>
      <sub><b>Architecture:</b> Multi-tenancy enforced directly at the database layer via PostgreSQL <i>Row-Level Security (RLS)</i>, backed by automated E2E tenant-isolation checks in CI.</sub><br><br>
      <code>Next.js</code> <code>Prisma</code> <code>PostgreSQL</code> <code>Playwright</code>
    </td>
    <td width="33.3%" valign="top">
      <b>Portal SST</b> &nbsp;<code>Microservices</code><br><br>
      <sub>Occupational health and safety platform for PPE delivery tracking, digital signatures, and psychosocial risk assessments (NR-1 compliance).</sub><br><br>
      <sub><b>Architecture:</b> Decoupled services operating behind an API Gateway, combining Node.js for transactional domain workflows and FastAPI for specialized data processing.</sub><br><br>
      <code>Node.js</code> <code>Python</code> <code>FastAPI</code> <code>PostgreSQL</code>
    </td>
    <td width="33.3%" valign="top">
      <b>ERP de Temporada</b> &nbsp;<code>Core ERP</code><br><br>
      <sub>Centralized property management system handling seasonal bookings, linen inventory, housekeeping schedules, and owner financial payouts.</sub><br><br>
      <sub><b>Architecture:</b> Modular monolith engineered around strict ACID transactions to guarantee consistency between operational calendars and financial reconciliation.</sub><br><br>
      <code>React</code> <code>Express</code> <code>Sequelize</code> <code>PostgreSQL</code>
    </td>
  </tr>
</table>

<br>

## Engineering & Operations

<img width="100%" alt="CI/CD Pipeline: Commit, Lint & Types, Tests, Migrations with RLS, E2E, Deploy, and Automated Restore Drills" src="./assets/pipeline-en.svg">

<table width="100%">
  <tr>
    <td width="50%" valign="top">
      <code>01</code> &nbsp;<b>Domain decoupled from infrastructure</b><br><br>
      <sub>Business rules and use cases are isolated from the HTTP transport layer and ORM specifics. Frameworks and external libraries act strictly as infrastructure details, simplifying testing and long-term maintenance.</sub>
    </td>
    <td width="50%" valign="top">
      <code>02</code> &nbsp;<b>Database-enforced tenant isolation</b><br><br>
      <sub><i>Row-Level Security (RLS)</i> policies are enforced directly inside PostgreSQL and audited automatically in the CI pipeline prior to deployment to prevent cross-tenant data leakage.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <code>03</code> &nbsp;<b>Controlled schema evolution</b><br><br>
      <sub>Every structural database change requires deterministic, versioned migrations reviewed via Pull Request. Automatic schema synchronization is strictly disabled in production environments.</sub>
    </td>
    <td width="50%" valign="top">
      <code>04</code> &nbsp;<b>Verified disaster recovery</b><br><br>
      <sub>A backup is only valid once restoration is proven. Scheduled database snapshots are paired with automated restore drills that provision an isolated instance and verify data integrity.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <code>05</code> &nbsp;<b>Risk-targeted testing strategy</b><br><br>
      <sub>Fast unit tests protect core domain calculations and business invariants, while integration and E2E suites target high-risk system boundaries (databases, queues, and external APIs).</sub>
    </td>
    <td width="50%" valign="top">
      <code>06</code> &nbsp;<b>Observability from initial deployment</b><br><br>
      <sub>Structured logging with request correlation context and exception tracking are configured before go-live, minimizing mean time to diagnosis in production.</sub>
    </td>
  </tr>
</table>

<br>

## Technology Stack

<table width="100%">
  <tr>
    <td width="24%"><sub><b>BACKEND & APIS</b></sub></td>
    <td width="76%">
      <img src="https://img.shields.io/badge/TypeScript-18181B?style=flat-square&logo=typescript&logoColor=3178C6" alt="TypeScript">
      <img src="https://img.shields.io/badge/Node.js-18181B?style=flat-square&logo=nodedotjs&logoColor=5FA04E" alt="Node.js">
      <img src="https://img.shields.io/badge/Express-18181B?style=flat-square&logo=express&logoColor=white" alt="Express">
      <img src="https://img.shields.io/badge/Python-18181B?style=flat-square&logo=python&logoColor=3776AB" alt="Python">
      <img src="https://img.shields.io/badge/FastAPI-18181B?style=flat-square&logo=fastapi&logoColor=009688" alt="FastAPI">
      <img src="https://img.shields.io/badge/Java-18181B?style=flat-square&logo=openjdk&logoColor=ED8B00" alt="Java">
      <img src="https://img.shields.io/badge/Spring_Boot-18181B?style=flat-square&logo=springboot&logoColor=6DB33F" alt="Spring Boot">
    </td>
  </tr>
  <tr>
    <td><sub><b>FRONTEND</b></sub></td>
    <td>
      <img src="https://img.shields.io/badge/Next.js-18181B?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js">
      <img src="https://img.shields.io/badge/React-18181B?style=flat-square&logo=react&logoColor=61DAFB" alt="React">
    </td>
  </tr>
  <tr>
    <td><sub><b>DATABASES & DATA LAYER</b></sub></td>
    <td>
      <img src="https://img.shields.io/badge/PostgreSQL-18181B?style=flat-square&logo=postgresql&logoColor=4169E1" alt="PostgreSQL">
      <img src="https://img.shields.io/badge/MySQL-18181B?style=flat-square&logo=mysql&logoColor=4479A1" alt="MySQL">
      <img src="https://img.shields.io/badge/SQL_Server-18181B?style=flat-square&logo=microsoftsqlserver&logoColor=CC2927" alt="SQL Server">
      <img src="https://img.shields.io/badge/Prisma-18181B?style=flat-square&logo=prisma&logoColor=white" alt="Prisma">
      <img src="https://img.shields.io/badge/Sequelize-18181B?style=flat-square&logo=sequelize&logoColor=52B0E7" alt="Sequelize">
      <img src="https://img.shields.io/badge/Redis-18181B?style=flat-square&logo=redis&logoColor=DC382D" alt="Redis">
    </td>
  </tr>
  <tr>
    <td><sub><b>INFRASTRUCTURE, QA & CI/CD</b></sub></td>
    <td>
      <img src="https://img.shields.io/badge/Docker-18181B?style=flat-square&logo=docker&logoColor=2496ED" alt="Docker">
      <img src="https://img.shields.io/badge/GitHub_Actions-18181B?style=flat-square&logo=githubactions&logoColor=2088FF" alt="GitHub Actions">
      <img src="https://img.shields.io/badge/Linux-18181B?style=flat-square&logo=linux&logoColor=FCC624" alt="Linux">
      <img src="https://img.shields.io/badge/Playwright-18181B?style=flat-square&logo=playwright&logoColor=2EAD33" alt="Playwright">
      <img src="https://img.shields.io/badge/Vitest-18181B?style=flat-square&logo=vitest&logoColor=6E9F18" alt="Vitest">
    </td>
  </tr>
</table>

<br>

---

<div align="center">
  <sub><b>Optima Sistemas</b> · <a href="https://optimasistemas.com">optimasistemas.com</a> &nbsp;·&nbsp; Direct contact: <a href="https://www.linkedin.com/in/matheus-henriquedev/">LinkedIn</a> &nbsp;·&nbsp; <a href="mailto:matheushenriqueds1223@gmail.com">matheushenriqueds1223@gmail.com</a></sub>
</div>
