#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# placement_manager.py
import random

class PlacementManager:
    def __init__(self, db):
        self.db = db
        self.statuses = ["placed", "ready", "not ready"]
        self.companies = ["Google", "Amazon", "TCS", "Wipro", "Infosys"]

    def insert_placement(self, i):
        placement_id = f"PL{i:03}"
        student_id = f"S{i:03}"
        mock_score = random.randint(0, 100)
        internships = random.randint(0, 3)
        status = random.choice(self.statuses)
        company = random.choice(self.companies) if status == "placed" else "NA"

        query = """
            INSERT INTO placement (
                placement_id, Stud_id, mock_interview_score,
                internships_completed, placement_status, company_name
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.db.execute_query(query, (placement_id, student_id, mock_score, internships, status, company))

    def populate_placements(self, count=500):
        for i in range(1, count + 1):
            self.insert_placement(i)
        self.db.commit()

