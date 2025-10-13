CREATE SCHEMA IF NOT EXISTS amd_PA;

CREATE TABLE IF NOT EXISTS amd_PA.PATIENT(
	nif VARCHAR(9) PRIMARY KEY,
	name VARCHAR(60) NOT NULL,
	birthdate DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS amd_PA.DISEASE(
	diseaseName VARCHAR(12) 
	CHECK (diseaseName IN ('myope', 'hypermetrope', 'astigmatic')) PRIMARY KEY
);


CREATE TABLE IF NOT EXISTS amd_PA.PATIENT_DISEASE(
	patient_nif VARCHAR(9) NOT NULL REFERENCES amd_PA.PATIENT(nif),
	diseaseName VARCHAR(12) NOT NULL REFERENCES amd_PA.DISEASE(diseaseName)
);

CREATE TABLE IF NOT EXISTS amd_PA.DOCTOR(
	n_doc SERIAL PRIMARY KEY,
	name VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS amd_PA.APPOINTMENT(
	id SERIAL PRIMARY KEY,
	patient_nif VARCHAR(9) NOT NULL REFERENCES amd_PA.PATIENT(nif),
	doctor_id INTEGER NOT NULL REFERENCES amd_PA.DOCTOR(n_doc),
	date Timestamp NOT NULL,
	age VARCHAR(14) NOT NULL
	CHECK (age IN ('young', 'presbyopic', 'pre-presbyopic')),
	astigmatic BOOLEAN NOT NULL,
	tear_rate VARCHAR(7) NOT NULL CHECK (tear_rate IN ('normal', 'reduced')),
	lenses VARCHAR(4) NOT NULL CHECK (lenses IN ('none', 'soft', 'hard'))	
);