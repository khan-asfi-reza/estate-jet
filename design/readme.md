# Database Design For Estatejet project

```postgresql
CREATE TABLE "Company" (
  "id" integer,
  "name" varchar
);

CREATE TABLE "User" (
  "id" integer UNIQUE PRIMARY KEY NOT NULL,
  "email" string,
  "first_name" string,
  "last_name" string,
  "phone_number" string,
  "country_code" string,
  "role" integer,
  "password" string,
  "company" Company
);

CREATE TABLE "Estate" (
  "id" integer,
  "name" integer,
  "address" integer,
  "host" User,
  "company" Company,
  "estate_type" integer,
  "geolocation" geolocation,
  "rooms" integer,
  "area" float8,
  "description" text,
  "cost_type" integer,
  "cost" integer,
  "amenities_json" JSON,
  "amenities" Amenity,
  "contract" Contract
);

CREATE TABLE "EstateDocument" (
  "id" integer,
  "estate" Estate,
  "document_type" integer,
  "title" varchar
);

CREATE TABLE "Document" (
  "id" integer,
  "name" varchar,
  "document" file,
  "document_thread" integer
);

CREATE TABLE "Feature" (
  "id" integer,
  "name" varchar,
  "value_type" integer
);

CREATE TABLE "EstateFeature" (
  "id" integer,
  "feature" Feature,
  "estate" Estate,
  "value" integer
);

CREATE TABLE "AmenityGroup" (
  "id" integer,
  "name" varchar
);

CREATE TABLE "Amenity" (
  "id" integer,
  "name" varchar,
  "group" AmenityGroup,
  "value_type" integer
);

CREATE TABLE "Contract" (
  "id" integer,
  "title" varchar,
  "hash" varchar,
  "contract_type" integer,
  "client" User,
  "company" Company,
  "created_at" datetime,
  "valid_until" datetime,
  "updated_at" datetime
);

CREATE TABLE "Images" (
  "estate" Estate,
  "id" integer,
  "file" varchar
);

CREATE TABLE "Verification" (
  "id" integer,
  "user" User,
  "user_image" file,
  "doc_image" file,
  "doc_type" integer
);

ALTER TABLE "Images" ADD CONSTRAINT "estate_image" FOREIGN KEY ("estate") REFERENCES "Estate" ("id");

ALTER TABLE "Verification" ADD CONSTRAINT "ver_user" FOREIGN KEY ("user") REFERENCES "User" ("id");

ALTER TABLE "Estate" ADD CONSTRAINT "estate_contract" FOREIGN KEY ("contract") REFERENCES "Contract" ("id");

ALTER TABLE "Amenity" ADD CONSTRAINT "amenity" FOREIGN KEY ("group") REFERENCES "AmenityGroup" ("id");

ALTER TABLE "Estate" ADD CONSTRAINT "estate_am" FOREIGN KEY ("amenities") REFERENCES "Amenity" ("id");

ALTER TABLE "User" ADD CONSTRAINT "estate_host" FOREIGN KEY ("id") REFERENCES "Estate" ("host");

ALTER TABLE "Company" ADD CONSTRAINT "estate_host" FOREIGN KEY ("id") REFERENCES "Estate" ("host");

ALTER TABLE "EstateFeature" ADD CONSTRAINT "feature_esf" FOREIGN KEY ("feature") REFERENCES "Feature" ("id");

ALTER TABLE "EstateFeature" ADD CONSTRAINT "feature_estate" FOREIGN KEY ("estate") REFERENCES "Estate" ("id");

ALTER TABLE "User" ADD CONSTRAINT "company_user" FOREIGN KEY ("company") REFERENCES "Company" ("id");

ALTER TABLE "Document" ADD CONSTRAINT "esdoc_doc" FOREIGN KEY ("document_thread") REFERENCES "EstateDocument" ("id");

ALTER TABLE "EstateDocument" ADD CONSTRAINT "esdoc_doc" FOREIGN KEY ("estate") REFERENCES "Estate" ("id");

ALTER TABLE "Contract" ADD CONSTRAINT "ctrct_user" FOREIGN KEY ("client") REFERENCES "User" ("id");

ALTER TABLE "Contract" ADD CONSTRAINT "cntrc_office" FOREIGN KEY ("company") REFERENCES "Company" ("id");


```