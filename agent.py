import json
import math
import random
import csv
import os

# ---------------- Utility Functions ----------------
def euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def random_delay():
    return random.randint(1, 10)

def get_warehouse_id(pkg):
    """
    Handles both 'warehouse' and 'warehouse_id'
    """
    if "warehouse" in pkg:
        return pkg["warehouse"]
    elif "warehouse_id" in pkg:
        return pkg["warehouse_id"]
    else:
        raise KeyError(f"No warehouse key found in package: {pkg}")

# ---------------- Load File ----------------
file_path = input("Enter JSON file path: ").strip()

if not os.path.exists(file_path):
    raise FileNotFoundError("❌ File not found")

with open(file_path, "r") as f:
    data = json.load(f)

# ---------------- Normalize Warehouses ----------------
if isinstance(data["warehouses"], list):
    warehouses = {w["id"]: w["location"] for w in data["warehouses"]}
else:
    warehouses = data["warehouses"]

# ---------------- Normalize Agents ----------------
if isinstance(data["agents"], list):
    agents = {a["id"]: a["location"] for a in data["agents"]}
else:
    agents = data["agents"]

# ---------------- Packages ----------------
packages = data["packages"]

# ---------------- New Agent Joins Mid-Day ----------------
agents["A4"] = [20, 80]

# ---------------- Assign Packages ----------------
assignments = {agent: [] for agent in agents}

for pkg in packages:
    wh_id = get_warehouse_id(pkg)
    wh_loc = warehouses[wh_id]

    nearest_agent = min(
        agents,
        key=lambda a: euclidean(agents[a], wh_loc)
    )

    assignments[nearest_agent].append(pkg)

# ---------------- Simulation ----------------
report = {}
routes = {}

for agent, start_pos in agents.items():
    total_distance = 0.0
    delivered = 0
    current_pos = start_pos[:]
    routes[agent] = []

    for pkg in assignments[agent]:
        wh_id = get_warehouse_id(pkg)
        wh = warehouses[wh_id]
        dest = pkg["destination"]

        total_distance += euclidean(current_pos, wh)
        total_distance += euclidean(wh, dest)
        total_distance += random_delay()

        routes[agent].append(f"{current_pos} -> {wh} -> {dest}")
        current_pos = dest
        delivered += 1

    efficiency = round(total_distance / delivered, 2) if delivered else 0

    report[agent] = {
        "packages_delivered": delivered,
        "total_distance": round(total_distance, 2),
        "efficiency": efficiency
    }

# ---------------- Best & Overall Efficiency ----------------
active_agents = [a for a in report if report[a]["packages_delivered"] > 0]

best_agent = min(active_agents, key=lambda a: report[a]["efficiency"])

overall_efficiency = round(
    sum(report[a]["efficiency"] for a in active_agents) / len(active_agents), 2
)

report["overall_efficiency"] = overall_efficiency
report["best_agent"] = best_agent

# ---------------- Save Outputs ----------------
base_name = os.path.splitext(os.path.basename(file_path))[0]

with open(f"{base_name}_report.json", "w") as f:
    json.dump(report, f, indent=2)

with open(f"{base_name}_top_agent.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Agent", "Packages Delivered", "Total Distance", "Efficiency"])
    writer.writerow([
        best_agent,
        report[best_agent]["packages_delivered"],
        report[best_agent]["total_distance"],
        report[best_agent]["efficiency"]
    ])

# ---------------- ASCII Routes ----------------
print("\n--- ASCII ROUTES ---")
for agent, paths in routes.items():
    print(f"\n{agent}:")
    for p in paths:
        print(p)

print("\n✅ Simulation Completed Successfully")
print(f"📊 Overall Efficiency: {overall_efficiency}")
print(f"🏆 Best Agent: {best_agent}")
print(f"📄 Report: {base_name}_report.json")
print(f"📁 CSV: {base_name}_top_agent.csv")