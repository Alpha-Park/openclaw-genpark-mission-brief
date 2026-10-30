# -*- coding: utf-8 -*-
"""
OpenClaw GenPark Mission Brief - Critical Path Method DAG Solver & Swarm Failure Surface Auditor
Standard Library only: math, typing.
Calculates forward/backward Critical Path Method (CPM) passes, detects zero-slack bottlenecks,
evaluates cosine similarity OKR alignment, and models compound swarm failure surfaces.
"""

import math
from typing import Dict, List, Any

class OpenClawGenParkMissionBrief:
    def __init__(self):
        pass

    def solve_critical_path_method(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Solves CPM DAG: computes Early Start (ES), Early Finish (EF), Late Start (LS),
        Late Finish (LF), and Total Float (Slack). Critical tasks have Slack == 0.
        Tasks schema: [{"id": "A", "duration": 4, "dependencies": []}, ...]
        """
        task_dict = {t["id"]: t for t in tasks}
        durations = {t["id"]: float(t.get("duration", 1.0)) for t in tasks}
        deps = {t["id"]: t.get("dependencies", []) for t in tasks}

        # 1. Forward Pass (Early Start & Early Finish)
        es = {}
        ef = {}
        
        # Topological sort order
        in_degree = {t["id"]: len(deps[t["id"]]) for t in tasks}
        queue = [tid for tid, deg in in_degree.items() if deg == 0]
        topo_order = []

        while queue:
            curr = queue.pop(0)
            topo_order.append(curr)
            # Find successors
            for tid, pred_list in deps.items():
                if curr in pred_list:
                    in_degree[tid] -= 1
                    if in_degree[tid] == 0:
                        queue.append(tid)

        # Compute ES and EF in topological order
        for tid in topo_order:
            pred_efs = [ef[p] for p in deps[tid] if p in ef]
            es[tid] = max(pred_efs) if pred_efs else 0.0
            ef[tid] = es[tid] + durations[tid]

        total_project_duration = max(ef.values()) if ef else 0.0

        # 2. Backward Pass (Late Start & Late Finish)
        lf = {}
        ls = {}
        # In reverse topological order
        for tid in reversed(topo_order):
            succ_lss = [ls[s] for s in topo_order if tid in deps[s] and s in ls]
            lf[tid] = min(succ_lss) if succ_lss else total_project_duration
            ls[tid] = lf[tid] - durations[tid]

        # 3. Slack & Critical Path Identification
        task_schedule = []
        critical_tasks = []
        for tid in topo_order:
            slack = round(ls[tid] - es[tid], 3)
            is_critical = abs(slack) < 1e-4
            if is_critical:
                critical_tasks.append(tid)

            task_schedule.append({
                "task_id": tid,
                "duration": durations[tid],
                "early_start": es[tid],
                "early_finish": ef[tid],
                "late_start": ls[tid],
                "late_finish": lf[tid],
                "slack": slack,
                "is_critical_path": is_critical
            })

        return {
            "total_project_duration": total_project_duration,
            "critical_path_tasks": critical_tasks,
            "critical_path_count": len(critical_tasks),
            "task_schedule": task_schedule
        }

    def align_okr_objective_vector(self, mission_deliverables: List[str],
                                   target_okrs: List[str]) -> Dict[str, Any]:
        """
        Calculates lexical token overlap cosine similarity between mission deliverables and target OKRs.
        """
        def tokenize(text_list):
            words = []
            for t in text_list:
                for w in t.lower().split():
                    clean = "".join(ch for ch in w if ch.isalnum())
                    if len(clean) > 2:
                        words.append(clean)
            return words

        d_words = tokenize(mission_deliverables)
        o_words = tokenize(target_okrs)

        vocab = sorted(list(set(d_words + o_words)))
        if not vocab:
            return {"cosine_similarity": 0.0, "alignment_grade": "NO_TOKENS"}

        v_d = [d_words.count(w) for w in vocab]
        v_o = [o_words.count(w) for w in vocab]

        dot = sum(a * b for a, b in zip(v_d, v_o))
        norm_d = math.sqrt(sum(a * a for a in v_d))
        norm_o = math.sqrt(sum(b * b for b in v_o))

        cosine_sim = dot / (norm_d * norm_o) if (norm_d * norm_o) > 0 else 0.0

        if cosine_sim >= 0.70:
            grade = "STRONG_STRATEGIC_ALIGNMENT"
        elif cosine_sim >= 0.40:
            grade = "MODERATE_ALIGNMENT"
        else:
            grade = "STRATEGIC_DRIFT_DETECTED"

        return {
            "cosine_similarity": round(cosine_sim, 4),
            "alignment_percentage": round(cosine_sim * 100.0, 2),
            "alignment_grade": grade,
            "deliverables_count": len(mission_deliverables),
            "okrs_count": len(target_okrs)
        }

    def calculate_swarm_risk_surface(self, critical_path_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Models compound failure probability across critical path tasks:
        P(Failure) = 1 - prod_{t in CriticalPath} (1 - P_fail(t))
        """
        if not critical_path_tasks:
            return {"compound_failure_probability": 0.0, "overall_reliability": 1.0}

        success_prob = 1.0
        task_risks = []

        for t in critical_path_tasks:
            # Default failure prob based on task duration/complexity
            p_fail = min(0.40, max(0.01, float(t.get("failure_probability", 0.05))))
            success_prob *= (1.0 - p_fail)
            task_risks.append({
                "task_id": t.get("task_id", "t_anon"),
                "task_failure_probability": p_fail,
                "task_reliability": round(1.0 - p_fail, 4)
            })

        failure_prob = 1.0 - success_prob

        if failure_prob >= 0.50:
            posture = "HAZARDOUS_NEEDS_REDUNDANCY"
        elif failure_prob >= 0.20:
            posture = "ELEVATED_CONTINGENCY_REQUIRED"
        else:
            posture = "ROBUST_MISSION_TOLERANCE"

        return {
            "critical_tasks_monitored": len(critical_path_tasks),
            "compound_mission_failure_probability": round(failure_prob, 4),
            "compound_mission_success_probability": round(success_prob, 4),
            "mission_risk_posture": posture,
            "per_task_breakdown": task_risks
        }
