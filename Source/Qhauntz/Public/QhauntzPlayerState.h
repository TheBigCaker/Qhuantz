
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
