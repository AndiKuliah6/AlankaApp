# Database workflow

## Local development

Use SQLite by keeping this in `.env`:

```env
DATABASE_URL=sqlite:///./alanka.db
AUTO_CREATE_SCHEMA=true
```

The application creates the local schema automatically.

## Supabase / PostgreSQL

1. Create a Supabase project.
2. Copy the PostgreSQL connection string into `.env` as `DATABASE_URL`.
3. Run `database/migrations/001_initial_schema.sql` in the Supabase SQL editor.
4. Run `database/migrations/002_add_customer_survey_description.sql` to add
	the customer survey description column (safe to run after the updated
	initial migration as well).
5. Set `AUTO_CREATE_SCHEMA=false`.
6. Start the application.

Never commit `.env` or a database password. The SQL migration is the source of truth for the initial PostgreSQL schema. Future changes must use a new numbered migration file, for example `002_add_quotation_versions.sql`.
