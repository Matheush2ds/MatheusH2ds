<img width="100%" alt="Matheus Henrique: Engenheiro de Software, Analista de Sistemas e Gestor de Projetos" src="./assets/header-pt.svg">

<div align="center">
  <br>
  <a href="https://optimasistemas.com"><kbd>&nbsp;&nbsp;optimasistemas.com&nbsp;&nbsp;</kbd></a>
  &nbsp;&nbsp;
  <a href="https://www.linkedin.com/in/matheus-henriquedev/"><kbd>&nbsp;&nbsp;LinkedIn&nbsp;&nbsp;</kbd></a>
  &nbsp;&nbsp;
  <a href="mailto:matheushenriqueds1223@gmail.com"><kbd>&nbsp;&nbsp;matheushenriqueds1223@gmail.com&nbsp;&nbsp;</kbd></a>
  &nbsp;&nbsp;
  <a href="./README.en.md"><kbd>&nbsp;&nbsp;English&nbsp;&nbsp;</kbd></a>
</div>

<br>

## Sobre

Engenheiro de software, analista de sistemas e fundador na **Optima Sistemas**, onde concebo, arquiteto e opero produtos SaaS B2B e plataformas de gestão operacional para empresas de serviços. Atuo em todo o ciclo de vida do software: da **análise de sistemas e gestão de projetos** (levantamento de requisitos, mapeamento de processos de negócio, viabilidade técnica e condução de entregas) à engenharia back-end e sustentação em produção, com foco em modelagem relacional, regras de domínio complexas, isolamento multi-tenant e integrações entre sistemas.

<table width="100%">
  <tr>
    <td width="25%" valign="top">
      <sub><b>OPERAÇÃO</b></sub><br>
      <code>Fundador @ Optima Sistemas</code>
    </td>
    <td width="25%" valign="top">
      <sub><b>GRADUAÇÃO</b></sub><br>
      <code>Ciência da Computação</code>
    </td>
    <td width="25%" valign="top">
      <sub><b>PÓS-GRADUAÇÃO</b></sub><br>
      <code>Arquitetura de Software & IA</code>
    </td>
    <td width="25%" valign="top">
      <sub><b>FOCO TÉCNICO</b></sub><br>
      <code>Back-end, Dados & Gestão</code>
    </td>
  </tr>
</table>

<br>

## Produtos & Arquitetura em Produção

Sistemas proprietários desenvolvidos e mantidos em produção na **Optima Sistemas**. Como são produtos comerciais B2B, os repositórios são privados; a topologia arquitetural, as fronteiras de domínio e as decisões de engenharia de cada plataforma estão detalhadas abaixo:

<img width="100%" alt="Arquitetura do Optima Control, Portal SST e ERP de Temporada" src="./assets/architecture-pt.svg">

<table width="100%">
  <tr>
    <td width="33.3%" valign="top">
      <b>Optima Control</b> &nbsp;<code>SaaS B2B</code><br><br>
      <sub>Plataforma de gestão operacional e financeira para controladoras de pragas e dedetizadoras.</sub><br><br>
      <sub><b>Arquitetura:</b> Multi-tenancy com isolamento imposto diretamente no banco via <i>Row-Level Security (RLS)</i> e validação E2E automatizada no pipeline de CI.</sub><br><br>
      <code>Next.js</code> <code>Prisma</code> <code>PostgreSQL</code> <code>Playwright</code>
    </td>
    <td width="33.3%" valign="top">
      <b>Portal SST</b> &nbsp;<code>Microsserviços</code><br><br>
      <sub>Plataforma de saúde e segurança do trabalho para gestão de entregas de EPIs, assinaturas digitais e avaliação de riscos psicossociais (NR-1).</sub><br><br>
      <sub><b>Arquitetura:</b> Serviços desacoplados operando atrás de um API Gateway, combinando Node.js para fluxos transacionais e FastAPI para processamento especializado.</sub><br><br>
      <code>Node.js</code> <code>Python</code> <code>FastAPI</code> <code>PostgreSQL</code>
    </td>
    <td width="33.3%" valign="top">
      <b>ERP de Temporada</b> &nbsp;<code>Core Operacional</code><br><br>
      <sub>Sistema centralizado de gestão de reservas, controle de enxoval, escala de governança/limpeza e repasse financeiro a proprietários.</sub><br><br>
      <sub><b>Arquitetura:</b> Monolito modular orientado a transações ACID para garantir consistência estrita entre calendário operacional e fechamento financeiro.</sub><br><br>
      <code>React</code> <code>Express</code> <code>Sequelize</code> <code>PostgreSQL</code>
    </td>
  </tr>
</table>

<br>

## Engenharia & Operação

<img width="100%" alt="Pipeline de integração, testes, migrations com RLS, deploy e ensaio de restauração" src="./assets/pipeline-pt.svg">

<table width="100%">
  <tr>
    <td width="50%" valign="top">
      <code>01</code> &nbsp;<b>Domínio desacoplado da infraestrutura</b><br><br>
      <sub>Regras de negócio e casos de uso isolados da camada HTTP e do ORM. Frameworks e bibliotecas externas atuam estritamente como detalhes de infraestrutura, facilitando evolução e testes.</sub>
    </td>
    <td width="50%" valign="top">
      <code>02</code> &nbsp;<b>Isolamento de dados garantido no banco</b><br><br>
      <sub>Políticas de <i>Row-Level Security (RLS)</i> aplicadas diretamente no PostgreSQL e auditadas automaticamente no CI antes de cada deploy para impedir vazamento entre tenants.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <code>03</code> &nbsp;<b>Evolução controlada de schema</b><br><br>
      <sub>Qualquer alteração estrutural de banco passa obrigatoriamente por migrations determinísticas e revisáveis em Pull Request. Zero sincronização automática em produção.</sub>
    </td>
    <td width="50%" valign="top">
      <code>04</code> &nbsp;<b>Recuperação de desastres validada</b><br><br>
      <sub>Backup só é válido quando a restauração é provada. Snapshots agendados são acompanhados de ensaios automatizados que sobem uma instância isolada e verificam a integridade dos dados.</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <code>05</code> &nbsp;<b>Testes direcionados ao risco real</b><br><br>
      <sub>Testes unitários rápidos blindam cálculos e invariantes de domínio, enquanto suítes de integração e E2E cobrem as fronteiras críticas (banco de dados, filas e APIs externas).</sub>
    </td>
    <td width="50%" valign="top">
      <code>06</code> &nbsp;<b>Observabilidade desde o primeiro deploy</b><br><br>
      <sub>Logs estruturados com contexto de correlação de requisição e rastreamento de exceções configurados antes de o sistema entrar no ar, reduzindo o tempo médio de diagnóstico em produção.</sub>
    </td>
  </tr>
</table>

<br>

## Stack Tecnológica

<table width="100%">
  <tr>
    <td width="24%"><sub><b>BACK-END & APIS</b></sub></td>
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
    <td><sub><b>FRONT-END</b></sub></td>
    <td>
      <img src="https://img.shields.io/badge/Next.js-18181B?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js">
      <img src="https://img.shields.io/badge/React-18181B?style=flat-square&logo=react&logoColor=61DAFB" alt="React">
    </td>
  </tr>
  <tr>
    <td><sub><b>BANCOS DE DADOS & DADOS</b></sub></td>
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
    <td><sub><b>INFRA, QA & CI/CD</b></sub></td>
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
  <sub><b>Optima Sistemas</b> · <a href="https://optimasistemas.com">optimasistemas.com</a> &nbsp;·&nbsp; Contato direto: <a href="https://www.linkedin.com/in/matheus-henriquedev/">LinkedIn</a> &nbsp;·&nbsp; <a href="mailto:matheushenriqueds1223@gmail.com">matheushenriqueds1223@gmail.com</a></sub>
</div>
