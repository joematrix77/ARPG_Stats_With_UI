import numpy as np
import pandas as pd

# Settings
max_level = 500
levels = np.arange(1, max_level + 1)

# Function to calculate stat gain based on level and thresholds
def generate_stat_curve(base_value, soft_cap_start, soft_cap_end, hard_cap_end, increment_rate=0.023, flat_value=1):
    stat_values = []
    
    reset_base = 1  # Starting point after reset
    increase_rate = 1.3  # 1.3% increment
    reset_limit_multiplier = 1.027  # 2.7% cap

    current_value = reset_base  # Initialize for post-150 logic

    for lvl in levels:
        if lvl == 1:
            value = 10  # Level 1 value
        elif lvl == 2:
            value = 15
        elif lvl == 3:
            value = 20
        elif lvl == 4:
            value = 25
        elif 100 <= lvl <= 149:
            value = 1  # Fixed value for levels 100 to 149
        elif lvl <= soft_cap_start:
            # Enhanced growth up to soft cap
            value = base_value + (base_value * ((lvl - 1) * increment_rate))
        elif soft_cap_start < lvl <= soft_cap_end:
            # Linear growth towards flat_value
            value = base_value + (soft_cap_start * (1 + increment_rate) ** (soft_cap_start - 1))
            value += (flat_value - value) * (lvl - soft_cap_start) / (soft_cap_end - soft_cap_start)
        elif lvl > soft_cap_end and lvl < 150:
            # After soft cap up to 149
            value = 1
            value += (1 * (increment_rate * (lvl - soft_cap_end)))
            if value < 1:
                value = 1
        elif lvl >= 150:
            # Increment by 1.3% each level
            current_value *= (1 + increase_rate)
            value = current_value

            # Check if it exceeds the reset cap (2.7% higher than reset base)
            if current_value > reset_base * reset_limit_multiplier:
                # Reset the base and current value to 1
                reset_base = 1
                current_value = reset_base
                value = current_value
        
        stat_values.append(round(value, 4))  # You can round to 2 if preferred
    
    return stat_values

# Generate all curves
hp_curve = generate_stat_curve(base_value=57, soft_cap_start=5, soft_cap_end=60, hard_cap_end=99)
mana_curve = generate_stat_curve(base_value=11, soft_cap_start=5, soft_cap_end=60, hard_cap_end=99)
stamina_curve = generate_stat_curve(base_value=13, soft_cap_start=5, soft_cap_end=60, hard_cap_end=99)
strength_curve = generate_stat_curve(base_value=0.25, soft_cap_start=5, soft_cap_end=20, hard_cap_end=99)
dexterity_curve = generate_stat_curve(base_value=0.2, soft_cap_start=5, soft_cap_end=20, hard_cap_end=99)
intelligence_curve = generate_stat_curve(base_value=0.30, soft_cap_start=5, soft_cap_end=20, hard_cap_end=99)
luck_curve = generate_stat_curve(base_value=0.15, soft_cap_start=5, soft_cap_end=20, hard_cap_end=99)
armor_curve = generate_stat_curve(base_value=0.10, soft_cap_start=5, soft_cap_end=20, hard_cap_end=99)
attack_curve = generate_stat_curve(base_value=0.30, soft_cap_start=5, soft_cap_end=20, hard_cap_end=99)

# SoulsMax curve - exponential growth without resetting
souls_curve = []
for lvl in levels:
    base_cost = 500
    exponent = 2.33
    souls_required = int(base_cost * (lvl ** exponent))
    souls_curve.append(souls_required)

# Combine into a DataFrame (rows = attributes, columns = levels)
curve_table = pd.DataFrame({
    "Attribute.HealthMax": hp_curve,
    "Attribute.ManaMax": mana_curve,
    "Attribute.StaminaMax": stamina_curve,
    "Attribute.StrengthMax": strength_curve,
    "Attribute.DexterityMax": dexterity_curve,
    "Attribute.IntelligenceMax": intelligence_curve,
    "Attribute.LuckMax": luck_curve,
    "Attribute.ArmorMax": armor_curve,
    "Attribute.AttackMax": attack_curve,
    "Attribute.SoulsMax": souls_curve
}).transpose()

# Column headers as integers (Levels 1 to 500)
curve_table.columns = levels

# Save to CSV
csv_filename = r"C:\Users\jcastro\Documents\Unreal Projects\ARPG_v5_Stats_Working\Plugins\ARPG_Stats\Content\Python\CT_LevelCurvesSouls.csv"
curve_table.to_csv(csv_filename)

print(f"Curve table saved as '{csv_filename}'")
import os
print(f"Saving to: {os.getcwd()}\\{csv_filename}")

