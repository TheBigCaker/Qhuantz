import unreal
import os

# -----------------------------------------------------------------------------
# SCRIPT 1: CREATE QHAUNTZ DATA LAYER
#
# Purpose:
# This script creates the foundational C++ header file:
#   Source/Qhauntz/Public/QhauntzData.h
#
# This file defines all the core structs and enums our game will use,
# such as FStressTrack and FConsequences.
# -----------------------------------------------------------------------------

unreal.log("--- Qhauntz Scripter: Starting Task 1 (Create QhauntzData.h) ---")

# --- 1. Define the C++ Code for QhauntzData.h ---
# We store the entire C++ file contents in this string.
CPP_CODE = """
#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "QhauntzData.generated.h"

/**
 * Defines the character's social and magical status (e.g., Fyemyn, Tyrmyn).
 * This determines how they interact with Aether.
 */
UENUM(BlueprintType)
enum class ECharacterStatus : uint8
{
    ECS_None    UMETA(DisplayName = "None"),
    ECS_Fyemyn  UMETA(DisplayName = "Fyemyn"),
    ECS_Tyrmyn  UMETA(DisplayName = "Tyrmyn")
};

/**
 * Struct to hold the four Affinity skill names,
 * linking a character's magical style to specific skills.
 */
USTRUCT(BlueprintType)
struct FQhauntzAffinity
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Data")
    FString Attack;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Data")
    FString Defend;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Data")
    FString Tend;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Data")
    FString NonCombat;
};

/**
 * Struct for a single Stress Track (e.g., Endurance, Resolve, or Aether).
 * Holds the available boxes and which ones are currently filled.
 */
USTRUCT(BlueprintType)
struct FStressTrack
{
    GENERATED_BODY()

    // The boxes available (e.g., [1, 2, 3])
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Data")
    TArray<int32> Tracks;

    // The boxes that are filled (e.g., [1])
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Data")
    TArray<int32> Filled;

    // Tracks that are temporary (e.g., from high stress)
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Data")
    TArray<int32> Temp;
};

/**
 * Struct for all Consequence slots.
 * We use an FString; if it's empty, the slot is free.
 */
USTRUCT(BlueprintType)
struct FConsequences
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Data")
    FString Endurance_Mild;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Data")
    FString Resolve_Mild;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Qhauntz Data")
    FString Aether_Mild;
};

/**
 * A "dummy" UObject class to make this file compilable as a header.
 * This is good practice for USTRUCT/UENUM-only files.
 */
UCLASS()
class QHAUNTZ_API UQhauntzData : public UObject
{
    GENERATED_BODY()
};
"""

# --- 2. Get Project Paths ---
# This finds your project's root folder (e.g., "C:/Projects/Qhauntz_Project/")
project_dir = unreal.SystemLibrary.get_project_directory()

# This gets the name of your project module (e.g., "Qhauntz")
# We assume the project name is "Qhauntz"
# If your project is named something else, you MUST change this line.
project_module_name = "Qhauntz" 

# Define the full path to the "Public" folder
public_dir = os.path.join(project_dir, "Source", project_module_name, "Public")

# Define the full path for the new file
file_path = os.path.join(public_dir, "QhauntzData.h")

unreal.log(f"Target file path is: {file_path}")

# --- 3. Create Directories and Write the File ---
try:
    # Create the "Source/Qhauntz/Public" directory tree if it doesn't exist
    os.makedirs(public_dir, exist_ok=True)

    # Write the C++ code string to the new .h file
    with open(file_path, "w") as f:
        f.write(CPP_CODE)

    unreal.log("--- SUCCESS! ---")
    unreal.log(f"Created new C++ file at: {file_path}")
    unreal.log("--- NEXT STEPS ---")
    unreal.log("1. In the Unreal Editor, go to 'Tools > Generate Visual Studio Project'.")
    unreal.log("2. Open the .sln file and build your project to make Unreal see the new file.")
    unreal.log("3. Let me know when you are ready for the next script!")

except Exception as e:
    unreal.log_error("--- SCRIPT FAILED! ---")
    unreal.log_error(f"Could not create file. Error: {e}")
