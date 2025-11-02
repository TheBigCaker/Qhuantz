
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
