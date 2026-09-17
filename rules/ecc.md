# Enterprise Cloud & Code Architecture (ECC)

## Architecture & Code Quality Protocol
Terapkan standar enterprise engineering untuk task backend, database, cloud, dan security:
- **Database & Query:** Hindari N+1 query, gunakan migration yang teruji, dan enforce ACID transaksi (`database-migrations`, `postgres-patterns`, `prisma-patterns`).
- **Security & Compliance:** Jalankan sanitasi input di boundary server, amankan auth tokens, dan cegah common vulnerabilities (`security-scan`, `security-review`).
- **Backend Patterns:** Terapkan clean architecture, error handling standar, dan idempotency (`backend-patterns`, `api-design`, `error-handling`).
