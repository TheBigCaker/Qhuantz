import unreal
import os

# -----------------------------------------------------------------------------
# SCRIPT 5: IMPLEMENT APPLYDAMAGE LOGIC
#
# Purpose:
# This script adds the first real game logic to our C++ "brain".
# It modifies the CombatComponent to add the core ApplyDamage function.
# This function will correctly apply damage to Stress Tracks and check
# for Consequences, as per the rulebook.
# -----------------------------------------------------------------------------

unreal.log("--- Qhauntz Scripter: Starting Task 5 (Implement ApplyDamage) ---")

# --- 1. Define Project Paths ---
project_dir = unreal.SystemLibrary.get_project_directory()
project_module_name = "Qhauntz" # <-- Ensure this matches your project name

public_dir = os.path.join(project_dir, "Source", project_module_name, "Public")
private_dir = os.path.join(project_dir, "Source", project_module_name, "Private")

component_h_path = os.path.join(public_dir, "QhauntzCombatComponent.h")
component_cpp_path = os.path.join(private_dir, "QhauntzCombatComponent.cpp")

# --- 2. Define the NEW C++ Code for QhauntzCombatComponent.h ---
# We are replacing the entire file with this new version
COMBAT_COMPONENT_H_CODE = """
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "QhauntzData.h" // We need our data definitions
#include "QhauntzCombatComponent.generated.h"

// Forward declare the PlayerState class to avoid circular dependencies
class AQhauntzPlayerState;

/**
 * UQhauntzCombatComponent
 *
 * This component manages all game mechanics, rules, and logic for a character.
 * It reads from and writes to its owning QhauntzPlayerState.
 * This is the "Rules Engine" of the game.
 */
UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class QHAUNTZ_API UQhauntzCombatComponent : public UActorComponent
{
	GENERATED_BODY()

public:	
	UQhauntzCombatComponent();

protected:
	virtual void BeginPlay() override;

	// A cached reference to the PlayerState that owns this component
	UPROPERTY(BlueprintReadOnly, Category = "Qhauntz")
	AQhauntzPlayerState* OwningPlayerState;

public:	
    // --- NEWLY ADDED FUNCTIONS ---

    /**
     * Applies a given amount of damage to the character.
     * This is the main function for taking damage.
     * @param DamageAmount The total shifts of damage to apply.
     * @param DamageType The type of damage (Physical or Magical).
     */
    UFUNCTION(BlueprintCallable, Category = "Qhauntz | Combat")
    void ApplyDamage(int32 DamageAmount, EStressType DamageType);

protected:
    /**
     * Helper function to find the smallest available stress box that
     * can absorb the incoming damage.
     * @param StressTrack The Stress Track to check (e.g., Endurance or Resolve).
     * @param DamageAmount The amount of damage we need to absorb.
     * @return The value of the box to fill (e.g., 2), or 0 if no box is suitable.
     */
    int32 FindBestStressBox(const FStressTrack& StressTrack, int32 DamageAmount);

    /**
     * Helper function to mark a stress box as filled.
     * @param StressTrack The Stress Track to modify.
     * @param BoxValue The value of the box to fill (e.g., 2).
     */
    void FillStressBox(UPARAM(ref) FStressTrack& StressTrack, int32 BoxValue);

    /**
     * Called when damage overflows stress tracks. Checks for a free
     * consequence slot and fills it.
     * @param DamageAmount The remaining damage to be absorbed by a Consequence.
     * @param DamageType The type of damage, to determine which slot to use.
     * @return The amount of damage *still* remaining (0 if absorbed).
     */
    int32 TakeConsequence(int32 DamageAmount, EStressType DamageType);
};
"""

# --- 3. Define the NEW C++ Code for QhauntzCombatComponent.cpp ---
# We are replacing the entire file with this new version
COMBAT_COMPONENT_CPP_CODE = """
#include "QhauntzCombatComponent.h"
#include "QhauntzPlayerState.h" // We need this to get/set data
#include "Kismet/GameplayStatics.h" // Not used yet, but good to have

UQhauntzCombatComponent::UQhauntzCombatComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

void UQhauntzCombatComponent::BeginPlay()
{
	Super::BeginPlay();

	// Cache our owning PlayerState
	OwningPlayerState = Cast<AQhauntzPlayerState>(GetOwner());
    if (!OwningPlayerState)
    {
        UE_LOG(LogTemp, Error, TEXT("QhauntzCombatComponent: Could not find owning QhauntzPlayerState!"));
    }
}

// --- NEW FUNCTION IMPLEMENTATIONS ---

void UQhauntzCombatComponent::ApplyDamage(int32 DamageAmount, EStressType DamageType)
{
    if (!OwningPlayerState)
    {
        UE_LOG(LogTemp, Error, TEXT("ApplyDamage: No OwningPlayerState!"));
        return;
    }

    // --- RULE: Magical damage hits Resolve first. Physical hits Endurance first. ---
    // (We will implement this rule logic in a future script. For now, we
    // will use a simple Resolve -> Endurance -> Consequence overflow.)

    int32 DamageRemaining = DamageAmount;
    UE_LOG(LogTemp, Log, TEXT("ApplyDamage: Taking %d damage."), DamageRemaining);

    // --- Step 1: Try to absorb with Resolve Stress Track ---
    int32 ResolveBoxToFill = FindBestStressBox(OwningPlayerState->Resolve, DamageRemaining);
    if (ResolveBoxToFill > 0)
    {
        FillStressBox(OwningPlayerState->Resolve, ResolveBoxToFill);
        UE_LOG(LogTemp, Log, TEXT("ApplyDamage: Filled Resolve box [%d]. Damage absorbed."), ResolveBoxToFill);
        DamageRemaining = 0; // Damage is fully absorbed by one box
    }

    // --- Step 2: If damage remains, try to absorb with Endurance ---
    if (DamageRemaining > 0)
    {
        int32 EnduranceBoxToFill = FindBestStressBox(OwningPlayerState->Endurance, DamageRemaining);
        if (EnduranceBoxToFill > 0)
        {
            FillStressBox(OwningPlayerState->Endurance, EnduranceBoxToFill);
            UE_LOG(LogTemp, Log, TEXT("ApplyDamage: Filled Endurance box [%d]. Damage absorbed."), EnduranceBoxToFill);
            DamageRemaining = 0; // Damage is fully absorbed
        }
    }

    // --- Step 3: If damage *still* remains, try to take a Consequence ---
    if (DamageRemaining > 0)
    {
        UE_LOG(LogTemp, Log, TEXT("ApplyDamage: %d damage remains. Attempting to take Consequence..."), DamageRemaining);
        DamageRemaining = TakeConsequence(DamageRemaining, DamageType);
    }

    // --- Step 4: If damage *STILL* remains, character is Taken Out ---
    if (DamageRemaining > 0)
    {
        UE_LOG(LogTemp, Warning, TEXT("ApplyDamage: %d damage remains. No free Stress or Consequence slots. CHARACTER IS TAKEN OUT."), DamageRemaining);
        // TODO: Implement "Taken Out" logic
    }
}

int32 UQhauntzCombatComponent::FindBestStressBox(const FStressTrack& StressTrack, int32 DamageAmount)
{
    // --- RULE: "You can absorb a hit by checking one or more stress boxes..."
    // --- "...you can only check one box if the value of that box is
    // --- equal to or greater than the value of the hit."
    // We will find the *smallest* available box that is big enough.
    
    int32 BestBox = 0;
    for (int32 Box : StressTrack.Tracks)
    {
        // Check if this box is (A) big enough and (B) not already filled
        if (Box >= DamageAmount && !StressTrack.Filled.Contains(Box))
        {
            if (BestBox == 0 || Box < BestBox)
            {
                BestBox = Box; // Found a smaller, better-fitting box
            }
        }
    }
    return BestBox;
}

void UQhauntzCombatComponent::FillStressBox(UPARAM(ref) FStressTrack& StressTrack, int32 BoxValue)
{
    if (!StressTrack.Filled.Contains(BoxValue))
    {
        StressTrack.Filled.Add(BoxValue);
        // TODO: Here we would call a function to check for Aether track gains.
        // CheckAetherTrackGains();
    }
}

int32 UQhauntzCombatComponent::TakeConsequence(int32 DamageAmount, EStressType DamageType)
{
    if (!OwningPlayerState) return DamageAmount;

    // --- RULE: Consequences absorb damage. Mild = 2, Moderate = 4, Severe = 6
    // We only have Mild slots right now, which absorb 2 damage.
    const int32 MildConsequenceValue = 2;

    // --- RULE: Try to use the matching Consequence type first ---
    // (This is a simplified version of the logic)

    if (DamageType == EStressType::EST_Resolve && OwningPlayerState->Consequences.Resolve_Mild.IsEmpty())
    {
        OwningPlayerState->Consequences.Resolve_Mild = TEXT("Default Mild Resolve Consequence");
        UE_LOG(LogTemp, Log, TEXT("TakeConsequence: Took Mild Resolve Consequence."));
        return DamageAmount - MildConsequenceValue;
    }
    
    if (DamageType == EStressType::EST_Endurance && OwningPlayerState->Consequences.Endurance_Mild.IsEmpty())
    {
        OwningPlayerState->Consequences.Endurance_Mild = TEXT("Default Mild Endurance Consequence");
        UE_LOG(LogTemp, Log, TEXT("TakeConsequence: Took Mild Endurance Consequence."));
        return DamageAmount - MildConsequenceValue;
    }
    
    if (OwningPlayerState->Consequences.Aether_Mild.IsEmpty())
    {
        OwningPlayerState->Consequences.Aether_Mild = TEXT("Default Mild Aether Consequence");
        UE_LOG(LogTemp, Log, TEXT("TakeConsequence: Took Mild Aether Consequence."));
        return DamageAmount - MildConsequenceValue;
    }

    // No free slots, return the full remaining damage
    UE_LOG(LogTemp, Warning, TEXT("TakeConsequence: No free Mild Consequence slots!"));
    return DamageAmount;
}
"""

# --- 4. Read, Verify, and Write Files ---
try:
    unreal.log("Verifying all files exist before modification...")
    
    # Check for both files
    if not os.path.exists(component_h_path):
        raise FileNotFoundError(f"Component.h not found at: {component_h_path}")
    if not os.path.exists(component_cpp_path):
        raise FileNotFoundError(f"Component.cpp not found at: {component_cpp_path}")
        
    unreal.log("All files verified. Proceeding with modifications...")

    # Write the .h file
    with open(component_h_path, "w") as f:
        f.write(COMBAT_COMPONENT_H_CODE)
    unreal.log(f"MODIFIED file: {component_h_path}")

    # Write the .cpp file
    with open(component_cpp_path, "w") as f:
        f.write(COMBAT_COMPONENT_CPP_CODE)
    unreal.log(f"MODIFIED file: {component_cpp_path}")

    unreal.log("--- SUCCESS! (Task 5) ---")
    unreal.log("--- NEXT STEPS ---")
    unreal.log("1. In the Unreal Editor, go to 'Tools > Generate Visual Studio Project'.")
    unreal.log("2. Open the .sln file and BUILD your project.")
    unreal.log("3. After the build, we will create a Blueprint of our PlayerState and test this new function!")

except Exception as e:
    unreal.log_error("--- SCRIPT FAILED! (Task 5) ---")
    unreal.log_error(f"Could not modify files. Error: {e}")

