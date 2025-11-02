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

/**
 * Heals the character by clearing Consequence slots or Stress boxes.
 * @param HealType The type of stress to heal (Endurance or Resolve).
 * @param HealShifts The total shifts of healing to apply.
 */
UFUNCTION(BlueprintCallable, Category = "Qhauntz | Combat")
void Tend(EStressType HealType, int32 HealShifts);


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

    /**
     * Checks the total number of filled Endurance and Resolve boxes
     * and adds temporary Aether tracks if a threshold is met.
     */
    void CheckAetherTrackGains();
};
