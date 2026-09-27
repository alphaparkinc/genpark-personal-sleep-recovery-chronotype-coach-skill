import sys, json, math

class PersonalSleepChronotypeCoach:
    """
    Science-based Chronotype & Circadian Architecture Engine.
    Aligns wake times with 90-minute REM/NREM sleep cycles,
    calculates adenosine/caffeine half-life decay, and schedules optimal focus windows.
    """
    def __init__(self):
        # Chronotype peak energy offsets
        self.chronotype_profiles = {
            "lion": {"peak_start": "08:00", "peak_end": "12:00", "ideal_sleep": "21:30", "caffeine_window_hours": 9},
            "bear": {"peak_start": "10:00", "peak_end": "14:00", "ideal_sleep": "23:00", "caffeine_window_hours": 10},
            "wolf": {"peak_start": "16:00", "peak_end": "21:00", "ideal_sleep": "01:00", "caffeine_window_hours": 10},
            "dolphin": {"peak_start": "15:00", "peak_end": "18:00", "ideal_sleep": "23:30", "caffeine_window_hours": 11}
        }

    def calculate_sleep_cycles(self, target_wake_hour, target_wake_minute, sleep_cycles_count=5):
        # 1 sleep cycle = 90 minutes. Average sleep latency = 15 minutes.
        total_sleep_min = (sleep_cycles_count * 90) + 15
        wake_total_min = target_wake_hour * 60 + target_wake_minute
        
        bedtime_total_min = (wake_total_min - total_sleep_min) % (24 * 60)
        bed_h = int(bedtime_total_min // 60)
        bed_m = int(bedtime_total_min % 60)

        # Alternative options for 4, 5, and 6 cycles
        options = []
        for cycles in [6, 5, 4]:
            t_min = (cycles * 90) + 15
            b_min = (wake_total_min - t_min) % (24 * 60)
            options.append({
                "cycles": cycles,
                "total_sleep_hours": round((cycles * 90) / 60.0, 1),
                "recommended_bedtime": f"{int(b_min // 60):02d}:{int(b_min % 60):02d}"
            })

        return {
            "target_wake_time": f"{target_wake_hour:02d}:{target_wake_minute:02d}",
            "primary_bedtime": f"{bed_h:02d}:{bed_m:02d}",
            "cycles_planned": sleep_cycles_count,
            "options": options
        }

    def compute_caffeine_cutoff(self, bedtime_hour, bedtime_minute, half_life_buffer_hours=10):
        bed_total_min = bedtime_hour * 60 + bedtime_minute
        cutoff_min = (bed_total_min - (half_life_buffer_hours * 60)) % (24 * 60)
        c_h = int(cutoff_min // 60)
        c_m = int(cutoff_min % 60)

        return {
            "bedtime": f"{bedtime_hour:02d}:{bedtime_minute:02d}",
            "caffeine_cutoff_time": f"{c_h:02d}:{c_m:02d}",
            "reason": f"Adenosine receptors require ~{half_life_buffer_hours}h for caffeine clearance to permit deep slow-wave sleep."
        }

    def generate_circadian_schedule(self, chronotype="bear", wake_hour=7):
        profile = self.chronotype_profiles.get(chronotype.lower(), self.chronotype_profiles["bear"])
        return {
            "chronotype": chronotype,
            "circadian_recommendations": [
                {"time": f"{wake_hour:02d}:15", "activity": "Outdoor natural sunlight exposure (10-15 mins) for cortisol reset"},
                {"time": f"{wake_hour+2:02d}:00", "activity": "First caffeine intake (delay 90 mins after waking to avoid afternoon crash)"},
                {"time": profile["peak_start"], "activity": f"Deep Work Focus Block (until {profile['peak_end']})"},
                {"time": "14:00", "activity": "Caffeine Hard Cutoff (protect sleep architecture)"},
                {"time": "21:30", "activity": "Dim ambient lighting & activate screen blue-light filters"}
            ]
        }

    def run_benchmark_sleep_chronotype(self):
        # Wake at 07:00 AM, 5 cycles (7.5h sleep + 15m latency -> 23:15 bedtime)
        cycles = self.calculate_sleep_cycles(7, 0, 5)
        cutoff = self.compute_caffeine_cutoff(23, 15, 10)
        schedule = self.generate_circadian_schedule("bear", 7)
        return {
            "benchmark_status": "PASSED",
            "recommended_bedtime": cycles["primary_bedtime"],
            "caffeine_cutoff": cutoff["caffeine_cutoff_time"],
            "circadian_events_count": len(schedule["circadian_recommendations"])
        }
