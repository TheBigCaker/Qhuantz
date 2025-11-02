import unreal
import os

# -----------------------------------------------------------------------------
# SCRIPT 3: CREATE QHAUNTZ COMBAT COMPONENT
#
# Purpose:
# This script creates the "brain" of our game logic:
#   - Source/Qhauntz/Public/QhauntzCombatComponent.h
#   - Source/Qhauntz/Private/QhauntzCombatComponent.cpp
#
# This component will be attached to our PlayerState and will contain all
# the functions that execute our TTRPG rules (ApplyDamage, Tend, etc.)
# -----------------------------------------------------------------------------

unreal.log("--- Qhauntz Scripter: Starting Task 3 (Create CombatComponent) ---")

# --- 1. Define the C++ Code for the .h (Header) file ---
HEADER_CODE = """
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
	// We will add all our rule functions here in future scripts.
	// For now, we just create the class.

	// Example function (we will implement this in the next script)
	// UFUNCTION(BlueprintCallable, Category = "Qhauntz | Combat")
	// void ApplyDamage(int32 DamageAmount, EStressType DamageType);
};
"""

# --- 2. Define the C++ Code for the .cpp (Implementation) file ---
CPP_CODE = """
#include "QhauntzCombatComponent.h"
#include "QhauntzPlayerState.h"
// We don't need GameplayStatics for this file, but it's good to know about.
// #include "Kismet/GameplayStatics.h"

UQhauntzCombatComponent::UQhauntzCombatComponent()
{
	// Set this component to be initialized when the game starts
	PrimaryComponentTick.bCanEverTick = false;
}

void UQhauntzCombatComponent::BeginPlay()
{
	Super::BeginPlay();

	// Get the Actor that owns this component (which should be our PlayerState)
	// and cast it to our specific C++ class.
	OwningPlayerState = Cast<AQhauntzPlayerState>(GetOwner());

	if (!OwningPlayerState)
	{
		UE_LOG(LogTemp, Error, TEXT("QhauntzCombatComponent: Could not find owning QhauntzPlayerState!"));
	}
	else
	{
		UE_LOG(LogTemp, Log, TEXT("QhauntzCombatComponent initialized successfully."));
	}
}
"""

# --- 3. Get Project Paths ---
project_dir = unreal.SystemLibrary.get_project_directory()
project_module_name = "Qhauntz" # <-- Ensure this matches your project name

public_dir = os.path.join(project_dir, "Source", project_module_name, "Public")
private_dir = os.path.join(project_dir, "Source", project_module_name, "Private")

# Define the full paths for the new files
header_path = os.path.join(public_dir, "QhauntzCombatComponent.h")
cpp_path = os.path.join(private_dir, "QhauntzCombatComponent.cpp")

# --- 4. Create Directories and Write the Files ---
try:
    # These directories should already exist, but we check just in case
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
	unreal.log("3. Let me know when you are ready to attach this new component to our PlayerState!")

except Exception as e:
	unreal.log_error("--- SCRIPT FAILED! ---")
	unreal.log_error(f"Could not create files. Error: {e}")

