#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# programming_manager.py
import random

class ProgrammingManager:
    def __init__(self, db):
        self.db = db
        self.languages = ["Python", "Java", "C++", "JavaScript", "Go", "Rust"]

    def insert_programming(self, i):
        prog_id = f"PR{i:03}"
        student_id = f"S{i:03}"
        lang = random.choice(self.languages)
        prob = random.randint(10, 200)
        asses = random.randint(0, 100)
        proj = random.randint(0, 5)
        certs = random.randint(0, 3)
        score = random.randint(0, 100)

        query = """
            INSERT INTO programming (
                programming_id, Stud_id, prog_lang, prob_solved,
                comp_asses, mini_proj, certifications, latest_score
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (prog_id, student_id, lang, prob, asses, proj, certs, score)
        self.db.execute_query(query, data)

    def populate_programming(self, count=500):
        for i in range(1, count + 1):
            self.insert_programming(i)
        self.db.commit()

