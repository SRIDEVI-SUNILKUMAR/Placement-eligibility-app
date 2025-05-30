DROP Database if exists placements;
CREATE DATABASE placements;
USE placements;
# "Students" table Creation
CREATE TABLE students (
    Student_id varchar(10) PRIMARY KEY,
    Full_Name VARCHAR(100),
    Age INT,
    Gender VARCHAR(10),
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(50),
    enrollment_year INT,
    course_batch VARCHAR(50),
    city VARCHAR(50),
    graduation_year INT
);
# "Programming" table Creation
CREATE TABLE programming (
    programming_id varchar(10) PRIMARY KEY,
    Stud_id varchar(10),
    prog_lang VARCHAR(10),
    prob_solved INT,
    comp_asses INT,
    mini_proj INT,
    certifications int,
    latest_score int,
    CONSTRAINT fk_students_ FOREIGN KEY (Stud_id) REFERENCES students (Student_id)
);
# "Soft Skills Table" table Creation
CREATE TABLE soft_skills (
    soft_skill_id varchar(10) PRIMARY KEY,
    Stud_id varchar(10),
    communication int,
    prob_solved INT,
    teamwork INT,
    presentation INT,
    leadership int,
    critical_thinking int,
    interpersonal_skills int,
    CONSTRAINT fk_soft_ FOREIGN KEY (Stud_id) REFERENCES students (Student_id)
);
#Placement table Creation
 CREATE TABLE placement (
    placement_id VARCHAR(10) PRIMARY KEY,
    Stud_id VARCHAR(10),
    mock_interview_score INT,
    internships_completed INT,
    placement_status VARCHAR(15),
    company_name VARCHAR(100),
    CONSTRAINT fk_placements_students FOREIGN KEY (Stud_id) REFERENCES students (Student_id)
);


