--==============
-- DB connection
--==============
\set dataBase postgres
;
\set userName postgres
;
\connect :dataBase :userName
;
--==========================
--==========================

COPY (SELECT * FROM amd_PA.lenses_dataset) TO 'C:/AMD/d01_lenses.tab' DELIMITER '	' CSV HEADER
;