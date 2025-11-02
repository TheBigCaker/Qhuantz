import unreal
import os
import sys
import re

# -----------------------------------------------------------------------------
# SCRIPT 8: IMPLEMENT MAGICAL ATTACK (2-ROLL SYSTEM)
#
# Purpose:
# This script adds the core "Magical Attack" logic from the rulebook.
# It adds two functions to QhauntzCombatComponent:
# 1. MagicalAttack_Roll1_Hit: Calculates the "to-hit" roll.
# 2. MagicalAttack_Roll2_Damage: Calculates the final damage based on Roll 1.
# -----------------------------------------------------------------------------

unreal.log("--- Qhauntz Scripter: Starting Task 8 (Implement Magical Attack) ---")

# --- Define C++ Code Snippets ---

# Added to QhauntzCombatComponent.h (Public)
PUBLIC_DECLARATIONS = '''

/**
 * Performs Roll 1 (The Hit) of a magical attack.
 * @param PhysicalSkillName The name of the physical skill to roll (Martial Arts, Marksmanship, Physique).
 * @param Roll1_4dF The dF roll result (e.g., -4 to +4).
 * @return The Hit Result category (<= -4 Misfire, -2 Miss, 1 Hit, 2 Crit, 3 Crit+, 4 Crit+Style).
 */
UFUNCTION(BlueprintCallable, Category = "Qhauntz | Combat | Rolls")
int32 MagicalAttack_Roll1_Hit(FString PhysicalSkillName, int32 Roll1_4dF);

/**
 * Performs Roll 2 (The Damage) of a magical attack, applying modifiers and Aether limits.
 * @param Roll1_Result The result from MagicalAttack_Roll1_Hit (this determines crits).
 * @param AetherSpent The amount of Aether used, which caps the damage.
 * @param Roll2_4dF The dF roll result (e.g., -4 to +4) for the damage roll.
 * @return The final damage (shifts) to be applied to the target.
 */
UFUNCTION(BlueprintCallable, Category = "Qhauntz | Combat | Rolls")
int32 MagicalAttack_Roll2_Damage(int32 Roll1_Result, int32 AetherSpent, int32 Roll2_4dF);
'''

# Added to QhauntzCombatComponent.cpp (End of file)
ROLL_1_IMPLEMENTATION = '''
int32 UQhauntzCombatComponent::MagicalAttack_Roll1_Hit(FString PhysicalSkillName, int32 Roll1_4dF)
{
if (!OwningPlayerState)
{
UE_LOG(LogTemp, Error, TEXT("MagicalAttack_Roll1: No OwningPlayerState!"));
return -100; // Return a deep failure code
}

// 1. Get Physical Skill value
const int32* PhysicalSkillBonusPtr = OwningPlayerState->Skills.Find(PhysicalSkillName);
int32 PhysicalSkillBonus = PhysicalSkillBonusPtr ? *PhysicalSkillBonusPtr : 0;
if (!PhysicalSkillBonusPtr)
{
UE_LOG(LogTemp, Warning, TEXT("MagicalAttack_Roll1: Skill '%s' not found on PlayerState, assuming 0."), *PhysicalSkillName);
}

// 2. Calculate Roll 1 Result
const int32 Roll1_Result = PhysicalSkillBonus + Roll1_4dF;
UE_LOG(LogTemp, Log, TEXT("MagicalAttack_Roll1: Rolling %s (%d) + %d = %d"), *PhysicalSkillName, PhysicalSkillBonus, Roll1_4dF, Roll1_Result);

// 3. Implement "Roll 1 (The Hit)" chart from rulebook
if (Roll1_Result <= -4)
{
// Misfire! Deal damage to self.
int32 SelfDamage = FMath::Abs(Roll1_Result) - 3; // -4 = 1 shift, -5 = 2 shifts
UE_LOG(LogTemp, Warning, TEXT("MagicalAttack_Roll1: MISFIRE! Taking %d Aether damage."), SelfDamage);
ApplyDamage(SelfDamage, EStressType::EST_Aether); // Apply misfire damage to self
return Roll1_Result; // Return the exact negative roll
}
else if (Roll1_Result <= -2)
{
// Miss
UE_LOG(LogTemp, Log, TEXT("MagicalAttack_Roll1: MISS."));
return -2; // Return standard "Miss" code
}
else if (Roll1_Result <= 1)
{
// Hit
UE_LOG(LogTemp, Log, TEXT("MagicalAttack_Roll1: HIT. Proceed to Roll 2."));
return 1; // Return standard "Hit" code
}
else if (Roll1_Result == 2)
{
// Crit Hit! (25% bonus)
UE_LOG(LogTemp, Log, TEXT("MagicalAttack_Roll1: CRIT HIT! (25%% Bonus). Proceed to Roll 2."));
return 2; // Return "Crit1" code
}
else if (Roll1_Result == 3)
{
// Crit Hit! (50% bonus)
UE_LOG(LogTemp, Log, TEXT("MagicalAttack_Roll1: CRIT HIT! (50%% Bonus). Proceed to Roll 2."));
return 3; // Return "Crit2" code
}
else // >= 4
{
// Crit with Style!
UE_LOG(LogTemp, Log, TEXT("MagicalAttack_Roll1: CRIT WITH STYLE! (50%% Bonus + Overcharge). Proceed to Roll 2."));
// TODO: Implement Overcharge advantage
return 4; // Return "Crit+Style" code
}
}
'''

# Added to QhauntzCombatComponent.cpp (End of file)
ROLL_2_IMPLEMENTATION = '''
int32 UQhauntzCombatComponent::MagicalAttack_Roll2_Damage(int32 Roll1_Result, int32 AetherSpent, int32 Roll2_4dF)
{
// If Roll 1 was a miss or misfire, no damage is dealt.
if (Roll1_Result < 1)
{
UE_LOG(LogTemp, Log, TEXT("MagicalAttack_Roll2: Roll 1 was a miss/misfire. No damage."));
return 0;
}

if (!OwningPlayerState)
{
UE_LOG(LogTemp, Error, TEXT("MagicalAttack_Roll2: No OwningPlayerState!"));
return 0;
}

// 1. Get Magical Attack Skill Name from Affinity
FString MagicSkillName = OwningPlayerState->Affinity.Attack;
if (MagicSkillName.IsEmpty())
{
UE_LOG(LogTemp, Error, TEXT("MagicalAttack_Roll2: PlayerState Affinity.Attack skill is not set!"));
return 0;
}

// 2. Get Magical Skill value
const int32* MagicSkillBonusPtr = OwningPlayerState->Skills.Find(MagicSkillName);
int32 MagicSkillBonus = MagicSkillBonusPtr ? *MagicSkillBonusPtr : 0;
if (!MagicSkillBonusPtr)
{
UE_LOG(LogTemp, Warning, TEXT("MagicalAttack_Roll2: Magic skill '%s' not found on PlayerState, assuming 0."), *MagicSkillName);
}

// 3. Calculate Roll 2 Result
const int32 Roll2_Result = MagicSkillBonus + Roll2_4dF;
UE_LOG(LogTemp, Log, TEXT("MagicalAttack_Roll2: Rolling %s (%d) + %d = %d"), *MagicSkillName, MagicSkillBonus, Roll2_4dF, Roll2_Result);

// 4. Check for damage failure (negative roll)
if (Roll2_Result < 0)
{
UE_LOG(LogTemp, Log, TEXT("MagicalAttack_Roll2: Roll 2 failed. No damage dealt."));
// TODO: Implement "fill Aether tracks" rule
return 0;
}

// 5. Apply Aether cap
// RULE: "limited by the Aether you spend"
int32 BaseDamage = FMath::Min(Roll2_Result, AetherSpent);
if (Roll2_Result > AetherSpent)
{
UE_LOG(LogTemp, Log, TEXT("MagicalAttack_Roll2: Damage capped by Aether spend (Rolled %d, Capped to %d)."), Roll2_Result, AetherSpent);
}

// 6. Apply Crit Multipliers from Roll 1
// RULE: +2 to +3 -> +25% / +50%. +4 -> +50%
if (Roll1_Result >= 4) // Crit with Style
{
BaseDamage = FMath::RoundToInt(BaseDamage * 1.5f);
UE_LOG(LogTemp, Log, TEXT("MagicalAttack_Roll2: Applying Crit w/ Style bonus. Damage is now %d."), BaseDamage);
}
else if (Roll1_Result == 3) // Crit Hit (50%)
{
BaseDamage = FMath::RoundToInt(BaseDamage * 1.5f);
UE_LOG(LogTemp, Log, TEXT("MagicalAttack_Roll2: Applying Crit+ bonus. Damage is now %d."), BaseDamage);
}
else if (Roll1_Result == 2) // Crit Hit (25%)
{
BaseDamage = FMath::RoundToInt(BaseDamage * 1.25f);
UE_LOG(LogTemp, Log, TEXT("MagicalAttack_Roll2: Applying Crit bonus. Damage is now %d."), BaseDamage);
}

UE_LOG(LogTemp, Log, TEXT("MagicalAttack_Roll2: Final Damage = %d"), BaseDamage);
return BaseDamage;
}
'''

def modify_header(header_path):
unreal.log(f"--- Modifying Header File: {header_path} ---")
if not os.path.exists(header_path):
unreal.log_error(f"File not found: {header_path}")
raise FileNotFoundError(f"File not found: {header_path}")

with open(header_path, 'r') as f:
content = f.read()

# Idempotency check
if "MagicalAttack_Roll1_Hit" in content:
unreal.log("Task 8: 'MagicalAttack_Roll1_Hit' function already found in .h file. Skipping header modification.")
return

# Find insertion point
insertion_marker = "void Tend(EStressType HealType, int32 HealShifts);"
if insertion_marker not in content:
raise Exception(f"Could not find insertion marker '{insertion_marker}' in .h file.")

# Insert new declarations
content = content.replace(insertion_marker, insertion_marker + PUBLIC_DECLARATIONS, 1)

with open(header_path, 'w') as f:
f.write(content)

unreal.log("Task 8: Successfully modified QhauntzCombatComponent.h")

def modify_cpp(cpp_path):
unreal.log(f"--- Modifying Cpp File: {cpp_path} ---")
if not os.path.exists(cpp_path):
unreal.log_error(f"File not found: {cpp_path}")
raise FileNotFoundError(f"File not found: {cpp_path}")

with open(cpp_path, 'r') as f:
content = f.read()

# Idempotency check
if "UQhauntzCombatComponent::MagicalAttack_Roll1_Hit" in content:
unreal.log("Task 8: 'MagicalAttack_Roll1_Hit' function already found in .cpp file. Skipping .cpp modification.")
return

# Append new function definitions to the end of the file
all_new_code = f"\n{ROLL_1_IMPLEMENTATION}\n{ROLL_2_IMPLEMENTATION}\n"
content += all_new_code

with open(cpp_path, 'w') as f:
f.write(content)

unreal.log("Task 8: Successfully modified QhauntzCombatComponent.cpp")

# --- Main Execution ---
def main():
try:
unreal.log("--- Qhauntz Scripter: Starting Task 8 (Implement Magical Attack) ---")

project_dir = unreal.SystemLibrary.get_project_directory()
project_module_name = "Qhauntz"

public_dir = os.path.join(project_dir, "Source", project_module_name, "Public")
private_dir = os.path.join(project_dir, "Source", project_module_name, "Private")

header_path = os.path.join(public_dir, "QhauntzCombatComponent.h")
cpp_path = os.path.join(private_dir, "QhauntzCombatComponent.cpp")

modify_header(header_path)
modify_cpp(cpp_path)

unreal.log("--- SUCCESS! (Task 8) ---")
unreal.log("All C++ files modified for 'Magical Attack'. Ready for build.")

except Exception as e:
unreal.log_error(f"--- SCRIPT FAILED! (Task 8) ---")
unreal.log_error(f"An unexpected error occurred: {e}")
unreal.log_error(f"Check file paths and C++ insertion markers.")
sys.exit(1) # Exit with an error code to stop any further automation

if __name__ == "__main__":
main()