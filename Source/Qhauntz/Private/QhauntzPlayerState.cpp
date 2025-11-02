
#include "QhauntzPlayerState.h"
#include "QhauntzCombatComponent.h" // <-- ADDED: Include the component

// --- ADDED: Constructor ---
AQhauntzPlayerState::AQhauntzPlayerState()
{
    // Create our "brain" component
    CombatComponent = CreateDefaultSubobject<UQhauntzCombatComponent>(TEXT("CombatComponent"));
}
