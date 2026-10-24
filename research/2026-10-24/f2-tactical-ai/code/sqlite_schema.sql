CREATE INDEX idx_description_award ON descriptive_rows(award_key);

CREATE INDEX idx_description_id ON descriptive_rows(award_id_explicit);

CREATE INDEX idx_description_tx ON descriptive_rows(transaction_key);

CREATE UNIQUE INDEX idx_enrichment_tx ON description_enrichment(transaction_key);

CREATE INDEX idx_source_action ON source_rows(action_date);

CREATE INDEX idx_source_award ON source_rows(award_key);

CREATE INDEX idx_source_award_id ON source_rows(award_id);

CREATE INDEX idx_source_entity ON source_rows(entity_name COLLATE NOCASE);

CREATE INDEX idx_source_entity_key ON source_rows(entity_key);

CREATE INDEX idx_source_tx ON source_rows(transaction_key);

CREATE UNIQUE INDEX idx_unique_row ON unique_transaction_rows(row_number);

CREATE UNIQUE INDEX idx_unique_tx ON unique_transaction_rows(transaction_key);

CREATE TABLE description_enrichment(
  transaction_key TEXT,
  first_description_row,
  source_count,
  description_text,
  psc_text,
  naics_text,
  agency_text,
  explicit_award_ids,
  distinct_award_keys,
  distinct_award_ids
);

CREATE TABLE descriptive_rows(id INTEGER PRIMARY KEY,source_file TEXT,source_row INTEGER,transaction_key TEXT,award_key TEXT,award_id_explicit TEXT,title TEXT,description TEXT,evidence_excerpt TEXT,psc TEXT,naics TEXT,awarding_agency_code TEXT,awarding_sub_agency_code TEXT,funding_agency_code TEXT,funding_sub_agency_code TEXT,parent_award_id TEXT,solicitation_identifier TEXT,identifiers_json TEXT,money_json TEXT,raw_locator TEXT,source_url TEXT,retrieved_at TEXT);

CREATE TABLE f2_candidate_awards(award_key TEXT PRIMARY KEY);

CREATE TABLE source_rows(row_number INTEGER PRIMARY KEY, transaction_key TEXT, award_key TEXT, award_id TEXT, award_type TEXT, award_id_parse_status TEXT, entity_key TEXT, entity_name TEXT, source TEXT, source_url TEXT, raw_locator TEXT, source_snapshot_sha256 TEXT, retrieved_at TEXT, eligibility TEXT, capability_tags TEXT, action_date TEXT, fiscal_year INTEGER, action_obligation_usd TEXT, obligation_cents INTEGER, description_text TEXT, psc_text TEXT, naics_text TEXT, agency_text TEXT, source_json TEXT);

CREATE TABLE unique_transaction_rows(
  transaction_key TEXT,
  row_number,
  source_record_count
);

CREATE VIEW transaction_details AS SELECT t.*,d.source_count AS description_source_count,d.first_description_row,r.award_id_explicit,r.awarding_agency_code,r.awarding_sub_agency_code,r.funding_agency_code,r.funding_sub_agency_code,r.parent_award_id,r.solicitation_identifier,r.money_json,r.title,r.description,r.evidence_excerpt,r.source_file AS description_source_file,r.source_row AS description_source_row FROM transactions t LEFT JOIN description_enrichment d USING(transaction_key) LEFT JOIN descriptive_rows r ON r.id=d.first_description_row;

CREATE VIEW transactions AS SELECT r.*,u.source_record_count FROM source_rows r JOIN unique_transaction_rows u USING(row_number);