#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# soft_skills_manager.py
import random

class SoftSkillsManager:
    def __init__(self, db):
        self.db = db

    def insert_soft_skills(self, i):
        ss_id = f"SS{i:03}"
        student_id = f"S{i:03}"
        data = [random.randint(0, 100) for _ in range(7)]  # Scores for 7 skills

        query = """
            INSERT INTO soft_skills (
                soft_skill_id, Stud_id, communication, prob_solved,
                teamwork, presentation, leadership, critical_thinking, interpersonal_skills
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.db.execute_query(query, (ss_id, student_id, *data))

    def populate_soft_skills(self, count=500):
        for i in range(1, count + 1):
            self.insert_soft_skills(i)
        self.db.commit()

