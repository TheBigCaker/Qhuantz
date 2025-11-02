import unreal
import os

# -----------------------------------------------------------------------------
# SCRIPT 2: CREATE QHAUNTZ PLAYER STATE
#
# Purpose:
# This script creates the C++ class that will act as our "Character Sheet":
#   - Source/Qhauntz/Public/QhauntzPlayerState.h
#   - Source/Qhauntz/Private/QhauntzPlayerState.cpp
#
# This class will hold all the data defined in QhauntzData.h.
# -----------------------------------------------------------------------------

unreal.log("--- Qhauntz Scripter: Starting Task 2 (Create PlayerState) ---")

# --- 1. Define the C++ Code for the .h (Header) file ---
HEADER_CODE = """
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerState.h"
#include "QhauntzData.h" // We MUST include our data definitions
#include "QhauntzPlayerState.generated.h"

/**
 * This class holds all persistent data for a player (their "Character Sheet").
 */
UCLASS()
class QHAUNTZ_API AQhauntzPlayerState : public APlayerState
{
    GENERATED_BODY()

public:
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

# --- 2. Define the C++ Code for the .cpp (Implementation) file ---
CPP_CODE = """
#include "QhauntzPlayerState.h"

// This file is intentionally blank for now.
// We are just defining the data in the .h file.
// Logic will be added to a new CombatComponent in a later script.
"""

# --- 3. Get Project Paths ---
project_dir = unreal.SystemLibrary.get_project_directory()
project_module_name = "Qhauntz" # <-- Ensure this matches your project name

public_dir = os.path.join(project_dir, "Source", project_module_name, "Public")
private_dir = os.path.join(project_dir, "Source", project_module_name, "Private")

# Define the full paths for the new files
header_path = os.path.join(public_dir, "QhauntzPlayerState.h")
cpp_path = os.path.join(private_dir, "QhauntzPlayerState.cpp")

# --- 4. Create Directories and Write the Files ---
try:
    # Create the "Source/Qhauntz/Public" and "Private" dirs if they don't exist
    os.makedirs(public_dir, exist_ok=True)
    os.makedirs(private_dir, exist_ok=True)

    # Write the .h file
    with open(header_path, "w") as f:
        f.write(HEADER_CODE)
    unreal.log(f"Created new HEADER file at: {header_path}")

    # Write the .cpp file
    with open(cpp_path, "w") as f:
        f.write(CPP_CODE)
    unreal.log(f"Created new CPP file at: {cpp_path}")

    unreal.log("--- SUCCESS! ---")
    unreal.log("--- NEXT STEPS ---")
    unreal.log("1. In the Unreal Editor, go to 'Tools > Generate Visual Studio Project'.")
    unreal.log("2. Open the .sln file and BUILD your project.")
    unreal.log("3. Let me know when you are ready for the next script!")

except Exception as e:
    unreal.log_error("--- SCRIPT FAILED! ---")
    unreal.log_error(f"Could not create files. Error: {e}")
