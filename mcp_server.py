import sys, json
from client import PersonalSleepChronotypeCoach

def main():
    coach = PersonalSleepChronotypeCoach()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(coach.run_benchmark_sleep_chronotype(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "calculate_sleep_cycles", "description": "Calculate 90-minute sleep cycle bedtime windows."},
                        {"name": "compute_caffeine_cutoff", "description": "Determine afternoon caffeine cutoff time."},
                        {"name": "generate_circadian_schedule", "description": "Generate daylight and focus schedule for chronotype."},
                        {"name": "run_benchmark_sleep_chronotype", "description": "Run sleep coach benchmark."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "calculate_sleep_cycles":
                    out = coach.calculate_sleep_cycles(args.get("target_wake_hour", 7), args.get("target_wake_minute", 0), args.get("sleep_cycles_count", 5))
                elif tname == "compute_caffeine_cutoff":
                    out = coach.compute_caffeine_cutoff(args.get("bedtime_hour", 23), args.get("bedtime_minute", 0), args.get("half_life_buffer_hours", 10))
                elif tname == "generate_circadian_schedule":
                    out = coach.generate_circadian_schedule(args.get("chronotype", "bear"), args.get("wake_hour", 7))
                elif tname == "run_benchmark_sleep_chronotype":
                    out = coach.run_benchmark_sleep_chronotype()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
