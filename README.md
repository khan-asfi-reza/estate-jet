<div align="center">
  <h1> estatejet </h1>
  <p> Real Estate Website Powered By FastAPI </p>
  <img src="https://github.com/khan-asfi-reza/estate-jet/actions/workflows/CI.yml/badge.svg">  
</div>  

## Stacks

1. FastAPI
2. Postgresql
3. VueJs

## Database Model

<img src="https://raw.githubusercontent.com/khan-asfi-reza/estate-jet/master/design/dbdesign.png">  

## Todo
- [x] Create User Model
- [ ] JWT Authentication
- [ ] JWT Security Middlewares
- [ ] All Model Integrations
- [ ] Model Tests


## Installation

1. Create Database

Install Postgresql

For Mac

```shell
brew install postgresql

brew services start postgresql
```

For Windows Visit Postgres website

2. Create Database

```sql
CREATE DATABASE estatejet;
CREATE USER estatejet WITH PASSWORD 'estatejet';

ALTER ROLE django SET client_encoding TO 'utf8';
ALTER ROLE django SET default_transaction_isolation TO 'read committed';
ALTER ROLE django SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE estatejet TO estatejet;
ALTER USER django CREATEDB;
```

3. Set ENV Variable

```

```