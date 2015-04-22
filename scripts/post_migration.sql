USE archiprod;
DROP TABLE evenement_dump;
DROP TABLE video_volume2;
DROP TABLE volume2;
DROP TABLE note_programme2;

USE acanthes_db;
ALTER TABLE intervenant CONVERT TO CHARACTER SET 'latin1';
ALTER TABLE intervenant CONVERT TO CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci';