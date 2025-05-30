#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# main.py
from database import DatabaseConnector
from student_manager import StudentManager
from programming_manager import ProgrammingManager
from soft_skills_manager import SoftSkillsManager
from placement_manager import PlacementManager

if __name__ == "__main__":
    db = DatabaseConnector('127.0.0.1', 'root', 'Jaya7494@123', 'placements')

    student_mgr = StudentManager(db)
    programming_mgr = ProgrammingManager(db)
    soft_skills_mgr = SoftSkillsManager(db)
    placement_mgr = PlacementManager(db)

    student_mgr.populate_students()
    programming_mgr.populate_programming()
    soft_skills_mgr.populate_soft_skills()
    placement_mgr.populate_placements()

    db.close()

