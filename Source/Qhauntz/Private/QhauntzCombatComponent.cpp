
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
