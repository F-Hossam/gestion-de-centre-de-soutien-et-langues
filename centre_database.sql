-- create table etudiant (
--     id_etudiant int primary key auto_increment,
--     nom varchar(20) not null ,
--     prenom varchar(20) not null ,
--     date_naiss date ,
--     niveau varchar(40) DEFAULT NULL
--     ); 

-- create table departement (
--     id_departement int primary key auto_increment,
--     libelle varchar(20) not null 
--     );
--     
-- create table enseignent (
--     matricule int primary key auto_increment,
--     nom varchar(20) not null ,
--     prenom varchar(20) not null 
--     );
-- create table formation (
--     num int primary key ,
--     nom varchar(20) not null );

-- create table seance (
--     codee int primary key auto_increment,
--     datee date ,
--     heure time ,
--     typee varchar(20) not null );

-- create table groupe (
-- 	codeg int primary key auto_increment 
--     );

-- alter table groupe 
-- add column idf int ;


-- ALTER TABLE groupe
-- ADD CONSTRAINT fk_groupe_formation
-- FOREIGN KEY (idf) REFERENCES formation (num);

-- create table grpetudiant (
--     id_etudianti int ,
--     codeg int ,
--     FOREIGN KEY (id_etudianti) REFERENCES etudiant (id_etudiant),
--     FOREIGN KEY (codeg) REFERENCES groupe (codeg),
--     PRIMARY KEY (id_etudianti,codeg)
--     ); 

-- create table inscription (
--     id_etudianti int ,
--     id_departementi int ,
--     date_insci date ,
--     solde int ,
--     FOREIGN KEY (id_etudianti) REFERENCES etudiant (id_etudiant),
--     FOREIGN KEY (id_departementi) REFERENCES departement (id_departement),
--     PRIMARY KEY (id_etudianti,id_departementi)
--     ); 

-- ALTER TABLE enseignent
-- ADD COLUMN numf int ;


-- ALTER TABLE enseignent
-- ADD CONSTRAINT fk_enseignent_formation
-- FOREIGN KEY (numf) REFERENCES formation (num);


-- ALTER TABLE formation
-- ADD COLUMN idep int ;

-- ALTER TABLE formation
-- ADD CONSTRAINT fk_departement_formation
-- FOREIGN KEY (idep) REFERENCES departement (id_departement);


-- alter table seance
-- add column grp int ;


-- ALTER TABLE seance
-- ADD CONSTRAINT fk_seance_grp
-- FOREIGN KEY (grp) REFERENCES groupe (codeg);


-- alter table groupe 
-- add column matr int ;


-- ALTER TABLE groupe 
-- ADD CONSTRAINT fk_groupe_enseignent
-- FOREIGN KEY (matr) REFERENCES enseignent (matricule);


-- create table assister (
--     id_etudianta int ,
--     codeea int ,
--     presence boolean default TRUE ,
--     FOREIGN KEY (id_etudianta) REFERENCES etudiant (id_etudiant),
--     FOREIGN KEY (codeea) REFERENCES seance(codee),
--     PRIMARY KEY (id_etudianta,codeea)
--     ); 

-- ALTER TABLE grpetudiant
-- ADD COLUMN consecutive_absences INT DEFAULT 0;


-- alter table inscription 
-- add column test boolean;

-- alter table formation 
-- add column niveau_f varchar(20) DEFAULT NULL ;


-- INSERT INTO departement (libelle) VALUES 
-- ('Soutient'),
-- ('Langues'),
-- ('Skills');


-- INSERT INTO formation (num,nom,niveau_f,idep) VALUES 
-- (1,'Math','2Bac',1),
-- (2,'Math','1Bac',1),
-- (3,'Math','TC',1),
-- (4,'Math','3Col',1),
-- (5,'Physique','2Bac',1),
-- (6,'Physique','1Bac',1),
-- (7,'Physique','TC',1),
-- (8,'Physique','3Col',1),
-- (9,'SVT','2Bac',1),
-- (10,'SVT','1Bac',1),
-- (11,'SVT','TC',1),
-- (12,'SVT','3Col',1),
-- (13,'Francais','1Bac',1),
-- (14,'Francais','3Col',1),
-- (15,'Anglais','2Bac',1),
-- (16,'Arabe','1Bac',1),
-- (17,'Arabe','3Col',1),
-- (18,'philosophie','2Bac',1),
-- (19,'Francais','autre',2),
-- (20,'Anglais','autre',2),
-- (21,'allemand','autre',2),
-- (22,'Informatique','autre',3),
-- (23,'Microsoft Office','autre',3),
-- (24,'soft skills','autre',3);


-- INSERT INTO groupe (codeg,idf) VALUES 
-- (1,23),
-- (2,20),
-- (3,1),
-- (4,6),
-- (5,14);

-- drop table inscription;
-- create table inscription (
--     id_etudianti int ,
--     id_departementi int ,
--     id_form int ,
--     date_insci date ,
--     solde int ,
--     FOREIGN KEY (id_etudianti) REFERENCES etudiant (id_etudiant),
--     FOREIGN KEY (id_departementi) REFERENCES departement (id_departement),
--     PRIMARY KEY (id_etudianti,id_departementi,id_form)
--     );

-- alter table inscription 
-- add column test boolean;

-- SELECT codeg
-- FROM grpetudiant
-- WHERE codeg IN (
--     SELECT codeg
--     FROM groupe
--     WHERE idf = 1
-- )
-- GROUP BY codeg
-- HAVING COUNT(id_etudianti) < 8;

-- ALTER TABLE seance AUTO_INCREMENT = 1;

-- ALTER TABLE seance
-- CHANGE COLUMN datee jour VARCHAR(20);

-- INSERT INTO seance (jour, heure, grp) VALUES ('lundi', '6:00', 2);


