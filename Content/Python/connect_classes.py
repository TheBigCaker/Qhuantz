import unreal
import os

# -----------------------------------------------------------------------------
# SCRIPT 4: CONNECT PLAYERSTATE AND COMBATCOMPONENT
#
# Purpose:
# This is a "bigger change" script that MODIFIES existing files.
# 1. Adds the UQhauntzCombatComponent to the AQhauntzPlayerState.
# 2. Makes the AQhauntzPlayerState Blueprintable.
# 3. Adds "GameplayAbilities" to our .Build.cs for future use.
# -----------------------------------------------------------------------------

unreal.log("--- Qhauntz Scripter: Starting Task 4 (Connecting Classes) ---")

# --- 1. Define Project Paths ---
project_dir = unreal.SystemLibrary.get_project_directory()
project_module_name = "Qhauntz" # <-- Ensure this matches your project name

public_dir = os.path.join(project_dir, "Source", project_module_name, "Public")
private_dir = os.path.join(project_dir, "Source", project_module_name, "Private")
build_cs_path = os.path.join(project_dir, "Source", project_module_name, "Qhauntz.Build.cs")

player_state_h_path = os.path.join(public_dir, "QhauntzPlayerState.h")
player_state_cpp_path = os.path.join(private_dir, "QhauntzPlayerState.cpp")

# --- 2. Define the NEW C++ Code for QhauntzPlayerState.h ---
# We are replacing the entire file with this new version
PLAYER_STATE_H_CODE = """
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerState.h"
#include "QhauntzData.h" // We MUST include our data definitions
#include "QhauntzPlayerState.generated.h"

// Forward declare our component class
class UQhauntzCombatComponent;

/**
 * This class holds all persistent data for a player (their "Character Sheet").
 * It is now Blueprintable, so we can create a BP version.
 */
UCLASS(Blueprintable) // <-- MODIFIED: Made Blueprintable
class QHAUNTZ_API AQhauntzPlayerState : public APlayerState
{
	GENERATED_BODY()

public:
    // --- ADDED: Constructor ---
    AQhauntzPlayerState();

    // --- ADDED: Combat Component ---
    // This is the "brain" that manages our rules.
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Qhauntz")
    UQhauntzCombatComponent* CombatComponent;

    // --- CORE INFO ---

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Stats")
    FString Maxim;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Stats")
    FString Imperative;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Stats")
    FString Guild;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Stats")
    ECharacterStatus Status;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Stats")
    FQhauntzAffinity Affinity;

    // --- SKILLS ---
    
    // We use a Map to store all skills by name.
    // This is flexible and easy to look up.
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Stats")
    TMap<FString, int32> Skills;

    // --- PLAYER ECONOMY ---

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Stats")
    int32 FatePoints;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Stats")
    int32 RefreshRate;

    // --- STRESS & CONSEQUENCES ---
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Stats | Stress")
    FStressTrack Endurance;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Stats | Stress")
    FStressTrack Resolve;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Stats | Stress")
    FStressTrack Aether;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Stats | Stress")
    FConsequences Consequences;
    
};
"""

# --- 3. Define the NEW C++ Code for QhauntzPlayerState.cpp ---
# We are replacing the entire file with this new version
PLAYER_STATE_CPP_CODE = """
#include "QhauntzPlayerState.h"
#include "QhauntzCombatComponent.h" // <-- ADDED: Include the component

// --- ADDED: Constructor ---
AQhauntzPlayerState::AQhauntzPlayerState()
{
    // Create our "brain" component
    CombatComponent = CreateDefaultSubobject<UQhauntzCombatComponent>(TEXT("CombatComponent"));
}
"""

# --- 4. Define the NEW C# Code for Qhauntz.Build.cs ---
# We are replacing the entire file with this new version
BUILD_CS_CODE = """
// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class Qhauntz : ModuleRules
{
	public Qhauntz(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
	
        // --- MODIFIED: Added GameplayAbilities, GameplayTags, GameplayTasks ---
		PublicDependencyModuleNames.AddRange(new string[] 
        { 
            "Core", 
            "CoreUObject", 
            "Engine", 
            "InputCore",
            "GameplayAbilities", // Added for future magic system
            "GameplayTags",      // Added for future magic system
            "GameplayTasks"      // Added for future magic system
        });

		PrivateDependencyModuleNames.AddRange(new string[] {  });

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });
		
		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
"""

# --- 5. Read, Verify, and Write Files ---
try:
    unreal.log("Verifying all files exist before modification...")
    
    # Check for all 3 files
    if not os.path.exists(player_state_h_path):
        raise FileNotFoundError(f"PlayerState.h not found at: {player_state_h_path}")
    if not os.path.exists(player_state_cpp_path):
        raise FileNotFoundError(f"PlayerState.cpp not found at: {player_state_cpp_path}")
    if not os.path.exists(build_cs_path):
        raise FileNotFoundError(f".Build.cs not found at: {build_cs_path}")
        
    unreal.log("All files verified. Proceeding with modifications...")

    # Write the .h file
    with open(player_state_h_path, "w") as f:
        f.write(PLAYER_STATE_H_CODE)
    unreal.log(f"MODIFIED file: {player_state_h_path}")

    # Write the .cpp file
    with open(player_state_cpp_path, "w") as f:
        f.write(PLAYER_STATE_CPP_CODE)
    unreal.log(f"MODIFIED file: {player_state_cpp_path}")

    # Write the .Build.cs file
    with open(build_cs_path, "w") as f:
        f.write(BUILD_CS_CODE)
    unreal.log(f"MODIFIED file: {build_cs_path}")

    unreal.log("--- SUCCESS! (Task 4) ---")
    unreal.log("--- NEXT STEPS ---")
    unreal.log("1. In the Unreal Editor, go to 'Tools > Generate Visual Studio Project'.")
    unreal.log("2. Open the .sln file and BUILD your project.")
    unreal.log("3. After the build, we can finally start writing our game logic!")

except Exception as e:
    unreal.log_error("--- SCRIPT FAILED! (Task 4) ---")
    unreal.log_error(f"Could not modify files. Error: {e}")
