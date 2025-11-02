import unreal
import os
import sys

# -----------------------------------------------------------------------------
# SCRIPT 7: IMPLEMENT TEND (HEALING) LOGIC
#
# Purpose:
# This script modifies the QhauntzCombatComponent C++ files to add
# the 'Tend' function and its helper methods, HealConsequence and HealStressBox.
# -----------------------------------------------------------------------------

unreal.log("--- Qhauntz Scripter: Starting Task 7 (Implement Tend) ---")

# --- Define C++ Code Snippets ---

# Added to QhauntzCombatComponent.h (Public)
PUBLIC_DECLARATIONS = '''

/**
 * Heals the character by clearing Consequence slots or Stress boxes.
 * @param HealType The type of stress to heal (Endurance or Resolve).
 * @param HealShifts The total shifts of healing to apply.
 */
UFUNCTION(BlueprintCallable, Category = "Qhauntz | Combat")
void Tend(EStressType HealType, int32 HealShifts);
'''

# Added to QhauntzCombatComponent.h (Protected)
PROTECTED_DECLARATIONS = '''

/**
 * Helper function to heal a Consequence slot.
 * @param HealType The type of Consequence to look for.
 * @param HealShiftsRemaining The pool of healing shifts, will be reduced if successful.
 */
void HealConsequence(EStressType HealType, int32& HealShiftsRemaining);

/**
 * Helper function to heal the smallest filled Stress box.
 * @param StressTrack The Stress Track to heal.
 * @param HealShiftsRemaining The pool of healing shifts, will be reduced if successful.
 */
void HealStressBox(UPARAM(ref) FStressTrack& StressTrack, int32& HealShiftsRemaining);
'''

# Added to QhauntzCombatComponent.cpp (End of file)
TEND_IMPLEMENTATION = '''
void UQhauntzCombatComponent::Tend(EStressType HealType, int32 HealShifts)
{
    if (!OwningPlayerState)
    {
        UE_LOG(LogTemp, Error, TEXT("Tend: No OwningPlayerState!"));
        return;
    }

    int32 HealShiftsRemaining = HealShifts;
    UE_LOG(LogTemp, Log, TEXT("Tend: Healing %d shifts of type %d."), HealShiftsRemaining, static_cast<int32>(HealType));

    // --- Step 1: Try to heal a Consequence first ---
    HealConsequence(HealType, HealShiftsRemaining);

    // --- Step 2: Use remaining shifts to heal Stress boxes ---
    if (HealShiftsRemaining > 0)
    {
        if (HealType == EStressType::EST_Endurance)
        {
            HealStressBox(OwningPlayerState->Endurance, HealShiftsRemaining);
        }
        else if (HealType == EStressType::EST_Resolve)
        {
            HealStressBox(OwningPlayerState->Resolve, HealShiftsRemaining);
        }
    }

    UE_LOG(LogTemp, Log, TEXT("Tend: Healing complete. %d shifts remaining."), HealShiftsRemaining);

    // After healing, we must re-check Aether gains
    // This is because removing filled boxes might reduce the total.
    CheckAetherTrackGains();
}
'''

# Added to QhauntzCombatComponent.cpp (End of file)
HEAL_CONSEQUENCE_IMPLEMENTATION = '''
void UQhauntzCombatComponent::HealConsequence(EStressType HealType, int32& HealShiftsRemaining)
{
    if (!OwningPlayerState) return;

    // --- RULE: Healing a Mild Consequence costs 2 shifts ---
    const int32 MildConsequenceHealCost = 2;

    if (HealShiftsRemaining < MildConsequenceHealCost)
    {
        // Not enough shifts to heal a Consequence
        return;
    }

    // Check the matching Consequence type
    if (HealType == EStressType::EST_Endurance && !OwningPlayerState->Consequences.Endurance_Mild.IsEmpty())
    {
        OwningPlayerState->Consequences.Endurance_Mild.Empty();
        HealShiftsRemaining -= MildConsequenceHealCost;
        UE_LOG(LogTemp, Log, TEXT("HealConsequence: Cleared Mild Endurance Consequence."));
    }
    else if (HealType == EStressType::EST_Resolve && !OwningPlayerState->Consequences.Resolve_Mild.IsEmpty())
    {
        OwningPlayerState->Consequences.Resolve_Mild.Empty();
        HealShiftsRemaining -= MildConsequenceHealCost;
        UE_LOG(LogTemp, Log, TEXT("HealConsequence: Cleared Mild Resolve Consequence."));
    }
    // Note: We don't check Aether_Mild, as Tend() is only for Endurance/Resolve.
}
'''

# Added to QhauntzCombatComponent.cpp (End of file)
HEAL_STRESS_BOX_IMPLEMENTATION = '''
void UQhauntzCombatComponent::HealStressBox(UPARAM(ref) FStressTrack& StressTrack, int32& HealShiftsRemaining)
{
    if (StressTrack.Filled.Num() == 0)
    {
        // No boxes to heal
        return;
    }

    // --- RULE: Heal the *smallest* filled box first ---
    // We will loop as long as we have shifts and boxes to heal.

    bool bHealedAtLeastOneBox = true;
    while (bHealedAtLeastOneBox && HealShiftsRemaining > 0 && StressTrack.Filled.Num() > 0)
    {
        bHealedAtLeastOneBox = false; // Assume we won't find a box this loop

        // Find the smallest filled box
        int32 SmallestFilledBox = 0;
        int32 SmallestBoxIndex = -1;

        for (int32 i = 0; i < StressTrack.Filled.Num(); ++i)
        {
            int32 CurrentBox = StressTrack.Filled[i];
            if (SmallestBoxIndex == -1 || CurrentBox < SmallestFilledBox)
            {
                SmallestFilledBox = CurrentBox;
                SmallestBoxIndex = i;
            }
        }

        // Now check if we can afford to heal this box
        // --- RULE: HealShifts must be >= box value ---
        if (SmallestBoxIndex != -1 && HealShiftsRemaining >= SmallestFilledBox)
        {
            // Heal it!
            StressTrack.Filled.RemoveAt(SmallestBoxIndex);
            HealShiftsRemaining -= SmallestFilledBox;
            bHealedAtLeastOneBox = true; // We healed one, so we should loop again
            UE_LOG(LogTemp, Log, TEXT("HealStressBox: Cleared stress box [%d]."), SmallestFilledBox);
        }
    }
}
'''

def modify_header(header_path):
    unreal.log(f"--- Modifying Header File: {header_path} ---")
    
    if not os.path.exists(header_path):
        unreal.log_error(f"File not found: {header_path}")
        raise FileNotFoundError(f"File not found: {header_path}")

    with open(header_path, 'r') as f:
        content = f.read()

    # --- FIX: ADD MISSING INCLUDE ---
    # EStressType is in QhauntzData.h, which was not included.
    include_marker = '#include "Components/ActorComponent.h"'
    include_addition = '#include "QhauntzData.h"'
    
    if include_marker not in content:
         raise Exception("Could not find include marker '#include ""Components/ActorComponent.h""' in .h file.")

    if include_addition not in content:
        content = content.replace(include_marker, f'{include_marker}\n{include_addition}', 1)
        unreal.log("Task 7 Fix: Added #include ""QhauntzData.h"" to .h file.")
    # ----------------------------------

    # Idempotency check for function
    if "void Tend(EStressType HealType, int32 HealShifts);" in content:
        unreal.log("Task 7: 'Tend' function already found in .h file. Skipping header modification.")
        return # Return *after* include check, in case include was missing

    # Find insertion points
    public_insertion_marker = "void ApplyDamage(int32 DamageAmount, EStressType DamageType);"
    protected_insertion_marker = "int32 TakeConsequence(int32 DamageAmount, EStressType DamageType);"

    if public_insertion_marker not in content:
        raise Exception("Could not find public insertion marker 'ApplyDamage' in .h file.")
    if protected_insertion_marker not in content:
        raise Exception("Could not find protected insertion marker 'TakeConsequence' in .h file.")

    # Insert new declarations
    content = content.replace(public_insertion_marker, public_insertion_marker + PUBLIC_DECLARATIONS, 1)
    content = content.replace(protected_insertion_marker, protected_insertion_marker + PROTECTED_DECLARATIONS, 1)

    with open(header_path, 'w') as f:
        f.write(content)
        
    unreal.log("Task 7: Successfully modified QhauntzCombatComponent.h")

def modify_cpp(cpp_path):
    unreal.log(f"--- Modifying Cpp File: {cpp_path} ---")
    
    if not os.path.exists(cpp_path):
        unreal.log_error(f"File not found: {cpp_path}")
        raise FileNotFoundError(f"File not found: {cpp_path}")

    with open(cpp_path, 'r') as f:
        content = f.read()

    # Idempotency check
    if "void UQhauntzCombatComponent::Tend(" in content:
        unreal.log("Task 7: 'Tend' function already found in .cpp file. Skipping .cpp modification.")
        return

    # Append new function definitions to the end of the file
    all_new_code = f"\n{TEND_IMPLEMENTATION}\n{HEAL_CONSEQUENCE_IMPLEMENTATION}\n{HEAL_STRESS_BOX_IMPLEMENTATION}\n"
    content += all_new_code

    with open(cpp_path, 'w') as f:
        f.write(content)
        
    unreal.log("Task 7: Successfully modified QhauntzCombatComponent.cpp")

# --- Main Execution ---
def main():
    try:
        unreal.log("--- Qhauntz Scripter: Starting Task 7 (Implement Tend) ---")
        
        project_dir = unreal.SystemLibrary.get_project_directory()
        project_module_name = "Qhauntz"
        
        public_dir = os.path.join(project_dir, "Source", project_module_name, "Public")
        private_dir = os.path.join(project_dir, "Source", project_module_name, "Private")
        
        header_path = os.path.join(public_dir, "QhauntzCombatComponent.h")
        cpp_path = os.path.join(private_dir, "QhauntzCombatComponent.cpp")

        modify_header(header_path)
        modify_cpp(cpp_path)

        unreal.log("--- SUCCESS! (Task 7) ---")
        unreal.log("All C++ files modified for 'Tend'. Ready for build.")
        
    except Exception as e:
        unreal.log_error(f"--- SCRIPT FAILED! (Task 7) ---")
        unreal.log_error(f"An unexpected error occurred: {e}")
        unreal.log_error(f"Check file paths and C++ insertion markers.")
        sys.exit(1) # Exit with an error code to stop any further automation

if __name__ == "__main__":
    main()