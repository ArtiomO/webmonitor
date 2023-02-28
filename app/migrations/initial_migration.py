initial_migration_script = """
CREATE TABLE websites (
	id serial PRIMARY KEY,
	url VARCHAR (255) UNIQUE NOT NULL,
	regexp VARCHAR (255) NOT NULL,
    interval SMALLINT NOT NULL,
	created_at TIMESTAMP NOT NULL
);

CREATE TABLE web_check_results (
	id serial PRIMARY KEY,
	request_timestamp TIMESTAMP NOT NULL,
	response_time INT NOT NULL,
	http_status_code INT NOT NULL DEFAULT 0,
	regexp_valid bool NOT NULL,
	website_id INT NOT NULL,
    FOREIGN KEY (website_id)
      REFERENCES websites (id)
);

CREATE INDEX check_results_request_timestamp_idx ON web_check_results (request_timestamp);
CREATE INDEX check_results_http_status_code_idx ON web_check_results (http_status_code);
CREATE INDEX check_results_regexp_valid_idx ON web_check_results (regexp_valid);
CREATE INDEX check_results_response_time_idx ON web_check_results (response_time);
"""
