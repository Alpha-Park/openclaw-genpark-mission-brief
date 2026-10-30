# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkMissionBrief

client = OpenClawGenParkMissionBrief()

TOOLS = [
    {
        "name": "solve_critical_path_method",
        "description": "Solves CPM DAG: early/late start and finish, float slack, and critical bottleneck tasks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tasks": {"type": "array", "items": {"type": "object"}}
            },
            "required": ["tasks"]
        }
    },
    {
        "name": "align_okr_objective_vector",
        "description": "Evaluates cosine similarity alignment between mission deliverables and corporate OKRs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mission_deliverables": {"type": "array", "items": {"type": "string"}},
                "target_okrs": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["mission_deliverables", "target_okrs"]
        }
    },
    {
        "name": "calculate_swarm_risk_surface",
        "description": "Models compound mission failure probability across critical path tasks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "critical_path_tasks": {"type": "array", "items": {"type": "object"}}
            },
            "required": ["critical_path_tasks"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "solve_critical_path_method":
            res = client.solve_critical_path_method(args["tasks"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "align_okr_objective_vector":
            res = client.align_okr_objective_vector(args["mission_deliverables"], args["target_okrs"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "calculate_swarm_risk_surface":
            res = client.calculate_swarm_risk_surface(args["critical_path_tasks"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
