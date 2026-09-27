import sys, json
from client import PersonalSleepChronotypeCoach

def main():
    print("Testing PersonalSleepChronotypeCoach...")
    coach = PersonalSleepChronotypeCoach()
    res = coach.run_benchmark_sleep_chronotype()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["recommended_bedtime"] == "23:15"
    assert res["caffeine_cutoff"] == "13:15"
    print("All Personal Sleep Chronotype Coach tests passed successfully!")

if __name__ == "__main__":
    main()
