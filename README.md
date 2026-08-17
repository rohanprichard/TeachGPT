# TeachGPT

An academic client-server chatbot system for educational institutions. Students can ask questions about course material, faculty can upload learning documents, and administrators can manage courses and content.

**Documentation:** [rohanprichard.github.io/TeachGPT](https://rohanprichard.github.io/TeachGPT/)

## Architecture at a glance

```text
React student/admin clients → FastAPI service → SQLAlchemy + Chroma → LLM and embedding providers
```

The repository contains the backend, separate student and admin React clients, database migrations, and a model-server component.

## Documentation map

- [System overview](docs/Overview.md)
- [Architecture](docs/Architecture.md)
- [Setup and installation](docs/Setup_and_Installation.md)
- [Backend API](docs/Backend_API.md)
- [Database model](docs/Database.md)
- [Deployment notes](docs/Deployment.md)

## Local development

This is a multi-service project with provider configuration and database dependencies. Start with the [setup guide](docs/Setup_and_Installation.md), then use the repository Docker scripts when your local environment matches their prerequisites.

Do not commit API keys, database URLs, uploaded educational material, or user data.

## Status

TeachGPT is a final-year project and a reference implementation, not a hosted multi-tenant service. Production use would require a security review, managed persistence, explicit data-retention rules, and deployment-specific authentication configuration.

## License

MIT
