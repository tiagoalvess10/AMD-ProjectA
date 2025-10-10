-- =========================
-- Populate PATIENT table
-- =========================
INSERT INTO amd.PATIENT(nif, name, birthdate) VALUES
('123456789', 'António José', '1990-03-19'),
('987654321', 'Ana Silva', '1980-03-27'),
('192837465', 'Mariana Oliveirra', '2005-02-14'),
('112233445', 'Pedro Almeida', '1975-07-30'),
('566778899', 'João Pedro', '1960-09-05');

-- =========================
-- Popular a tabela DISEASE
-- =========================
INSERT INTO amd.DISEASE(diseaseName) VALUES
('myope'),
('hypermetrope'),
('astigmatic');

-- =================================
-- Populate PATIENT_DISEASE table
-- =================================
INSERT INTO amd.PATIENT_DISEASE(patient_nif, diseaseName) VALUES
('123456789', 'myope'),
('987654321', 'hypermetrope'),
('192837465', 'astigmatic'),
('112233445', 'myope'),
('112233445', 'astigmatic'),
('566778899', 'hypermetrope');

-- =========================
-- Populate DOCTOR table
-- =========================
INSERT INTO amd.DOCTOR(name) VALUES
('Dr. Miguel Correia'),
('Dra. Sofia Costa'),
('Dra. Marta Sofia');

-- =========================
-- Populate APPOINTMENT table
-- =========================
INSERT INTO amd.APPOINTMENT(patient_nif, doctor_id, date, age, astigmatic, tear_rate, lenses) VALUES
('123456789', 1, '2024-10-10 10:00', 'young', FALSE, 'normal', 'soft'),
('987654321', 2, '2025-10-11 14:30', 'pre-presbyopic', FALSE, 'reduced', 'hard'),
('192837465', 1, '2024-10-12 09:00', 'young', TRUE, 'normal', 'soft'),
('112233445', 3, '2025-10-13 11:00', 'presbyopic', TRUE, 'reduced', 'hard'),
('566778899', 2, '2025-10-14 16:00', 'presbyopic', FALSE, 'normal', 'soft'),
('123456789', 2, '2025-10-10 10:00', 'young', FALSE, 'normal', 'soft'),
('192837465', 3, '2025-10-12 13:00', 'young', TRUE, 'normal', 'soft');
