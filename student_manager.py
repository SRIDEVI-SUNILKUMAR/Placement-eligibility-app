#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# student_manager.py
from faker import Faker
import random

class StudentManager:
    def __init__(self, db):
        self.db = db
        self.fake = Faker()
        self.genders = ["Male", "Female", "Other"]
        self.courses = ['DS', 'AI', 'ML', 'DS & AI', 'AI & ML']

    def insert_student(self, i):
        student_id = f"S{i:03}"
        gender = random.choice(self.genders)
        full_name = self.fake.name_male() if gender == "Male" else (
            self.fake.name_female() if gender == "Female" else self.fake.name()
        )
        age = random.randint(18, 30)
        email = self.fake.unique.email()
        phone = self.fake.msisdn()
        enrollment_year = random.randint(2020, 2025)
        course = random.choice(self.courses)
        city = self.fake.city()
        graduation_year = random.randint(2024, 2029)

        query = """
            INSERT INTO students (
                Student_id, Full_Name, Age, Gender, Email, Phone,
                enrollment_year, course_batch, city, graduation_year
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (student_id, full_name, age, gender, email, phone,
                enrollment_year, course, city, graduation_year)
        self.db.execute_query(query, data)

    def populate_students(self, count=500):
        for i in range(1, count + 1):
            self.insert_student(i)
        self.db.commit()

