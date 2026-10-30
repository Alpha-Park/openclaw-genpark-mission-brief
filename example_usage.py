# -*- coding: utf-8 -*-
from client import OpenClawGenParkMissionBrief

brief = OpenClawGenParkMissionBrief()

# 1. Critical Path Method
tasks = [
    {"id": "A", "duration": 3.0, "dependencies": []},
    {"id": "B", "duration": 4.0, "dependencies": ["A"]},
    {"id": "C", "duration": 2.0, "dependencies": ["A"]},
    {"id": "D", "duration": 5.0, "dependencies": ["B"]},
    {"id": "E", "duration": 1.0, "dependencies": ["C", "D"]}
]
cpm = brief.solve_critical_path_method(tasks)
print(f"Total Duration: {cpm['total_project_duration']}h, Critical Path: {cpm['critical_path_tasks']}")

# 2. OKR Alignment
deliverables = ["Deploy automated spot GPU broker with sub-millisecond bidding", "Publish zero-dependency Python MCP server"]
okrs = ["Scale automated AI compute infrastructure with high availability", "Launch standard open protocol tools for agent economy"]
align = brief.align_okr_objective_vector(deliverables, okrs)
print(f"\nOKR Alignment: {align['alignment_percentage']}% -> {align['alignment_grade']}")

# 3. Swarm Risk Surface
critical_items = [
    {"task_id": "A", "failure_probability": 0.05},
    {"task_id": "B", "failure_probability": 0.08},
    {"task_id": "D", "failure_probability": 0.12},
    {"task_id": "E", "failure_probability": 0.02}
]
risk = brief.calculate_swarm_risk_surface(critical_items)
print(f"\nCompound Risk: Failure Probability = {risk['compound_mission_failure_probability']*100:.1f}% ({risk['mission_risk_posture']})")
