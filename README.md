<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/header-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/header-light.svg">
  <img src="./assets/header-light.svg" width="100%" alt="Matheus Henrique — Desenvolvedor Full Stack, Analista de Sistemas e Fundador da Optima Sistemas">
</picture>

<p align="center">
  <a href="https://optimasistemas.com">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=15&duration=3200&pause=1000&color=6366F1&center=true&vCenter=true&width=520&lines=Desenvolvedor+Full+Stack+%26+Analista+de+Sistemas;Fundador+da+Optima+Sistemas+%E2%80%A2+SaaS+B2B;TypeScript+%E2%80%A2+Node.js+%E2%80%A2+Next.js+%E2%80%A2+PostgreSQL;Arquitetura+Multi-tenant+%26+Sistemas+de+Gest%C3%A3o" alt="Especialidades de Matheus Henrique: Desenvolvedor Full Stack, Analista de Sistemas, SaaS B2B, TypeScript, Node.js, Next.js e PostgreSQL" />
  </a>
</p>

<p align="center">
  <a href="https://optimasistemas.com">
    <img src="https://img.shields.io/badge/Optima_Sistemas-0F172A?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Site oficial da Optima Sistemas" />
  </a>
  <a href="https://www.linkedin.com/in/matheus-henriquedev/">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Perfil no LinkedIn de Matheus Henrique" />
  </a>
  <a href="mailto:matheushenriqueds1223@gmail.com">
    <img src="https://img.shields.io/badge/E--mail-1E293B?style=for-the-badge&logo=gmail&logoColor=white" alt="Enviar e-mail para Matheus Henrique" />
  </a>
  <a href="./README.en.md">
    <img src="https://img.shields.io/badge/English_Version-334155?style=for-the-badge&logo=translate&logoColor=white" alt="Read README in English" />
  </a>
</p>

---

## Sobre mim

Sou **desenvolvedor full stack**, analista de sistemas e fundador da **Optima Sistemas**, empresa especializada na criação, arquitetura e operação de **produtos SaaS B2B** e sistemas de gestão corporativa sob medida.

Atuo em todo o ciclo de desenvolvimento de software — da análise de requisitos, mapeamento de processos e modelagem de dados até o desenvolvimento front-end, construção de APIs back-end e sustentação em ambientes de produção. Meu foco técnico está em **interfaces funcionais**, **modelagem relacional avançada**, **regras de domínio complexas**, **isolamento multi-tenant** e **integração entre sistemas**.

> **Formação acadêmica:** Bacharel em Ciência da Computação, com pós-graduação em Arquitetura de Software e Inteligência Artificial.

---

## Produtos em produção

Plataformas proprietárias que idealizei, desenvolvo e mantenho na **Optima Sistemas**. Por serem produtos comerciais ativos, o código-fonte é privado; abaixo estão o contexto de negócio e as decisões de arquitetura de cada sistema.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/products-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/products-light.svg">
  <img src="./assets/products-light.svg" width="100%" alt="Arquitetura dos produtos Optima Control, Portal SST e ERP de Temporada">
</picture>

### Optima Control
<sub>Gestão operacional e financeira para empresas controladoras de pragas &nbsp;·&nbsp; Next.js, Prisma, PostgreSQL (RLS)</sub>

Plataforma SaaS multi-tenant onde o isolamento de dados entre clientes ocorre nativamente no **PostgreSQL** por meio de políticas de **Row-Level Security (RLS)**, validado automaticamente por uma suíte de testes E2E no pipeline de CI/CD.

### Portal SST
<sub>Saúde e segurança do trabalho: controle de EPIs, assinatura digital e risco psicossocial (NR-1) &nbsp;·&nbsp; API Gateway, Node.js, FastAPI, PostgreSQL</sub>

Arquitetura distribuída atrás de um **API Gateway**, combinando **Node.js** nos fluxos transacionais do dia a dia com **Python (FastAPI)** no processamento analítico e rotinas especializadas.

### ERP de Temporada
<sub>Centralização de reservas, controle de enxoval, escala de limpeza e repasse financeiro &nbsp;·&nbsp; React, Express, Sequelize, PostgreSQL</sub>

Monolito modular construído sobre **transações ACID**, garantindo consistência absoluta entre o calendário operacional de hospedagens e o fechamento financeiro dos proprietários.

---

## Como eu construo software

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/pipeline-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/pipeline-light.svg">
  <img src="./assets/pipeline-light.svg" width="100%" alt="Pipeline de engenharia de software: lint, testes unitários, migrations, E2E, deploy, observabilidade e backup">
</picture>

- **Domínio separado da infraestrutura:** Regras de negócio e casos de uso desacoplados da camada HTTP e do ORM. Framework é detalhe de borda.
- **Isolamento de dados garantido no banco:** Políticas de Row-Level Security (RLS) no PostgreSQL auditadas no CI antes de cada deploy.
- **Schema versionado:** Toda mudança estrutural vira migration revisada em pull request, sem sincronização automática em produção.
- **Backup só vale se restaura:** Snapshots agendados acompanhados de ensaios automáticos que sobem uma instância isolada e validam a integridade dos dados.
- **Teste onde está o risco:** Testes unitários rápidos para regras e invariantes do domínio; integração e E2E nas bordas críticas (banco de dados, filas e APIs externas).
- **Observabilidade desde o primeiro deploy:** Logs estruturados com correlação de requisição e rastreamento de exceções antes de o sistema entrar no ar.

---

## Stack tecnológica

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/stack-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/stack-light.svg">
  <img src="./assets/stack-light.svg" width="100%" alt="Stack tecnológica: TypeScript, Node.js, Express, Python, FastAPI, Java, Spring Boot, Next.js, React, PostgreSQL, MySQL, SQL Server, Prisma, Sequelize, Redis, Docker, GitHub Actions, Linux, Playwright e Vitest">
</picture>

<br>

<p align="center">
  <img height="165" src="https://github-readme-stats.vercel.app/api?username=Matheush2ds&show_icons=true&hide_border=true&bg_color=00000000&title_color=6366F1&icon_color=6366F1&text_color=64748B" alt="Estatísticas no GitHub de Matheus Henrique" />
  <img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Matheush2ds&layout=compact&hide_border=true&bg_color=00000000&title_color=6366F1&text_color=64748B" alt="Linguagens mais utilizadas por Matheus Henrique no GitHub" />
</p>

<br>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F172A,100:6366F1&height=90&section=footer" width="100%" alt="Rodapé visual" />
</p>

<p align="center">
  <sub><a href="https://optimasistemas.com"><strong>Optima Sistemas</strong></a> &nbsp;·&nbsp; Desenvolvimento Full Stack, Arquitetura SaaS e Software de Gestão sob Medida</sub>
</p>
