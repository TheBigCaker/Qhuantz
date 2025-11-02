
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
