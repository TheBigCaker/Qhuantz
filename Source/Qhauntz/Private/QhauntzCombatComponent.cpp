#include "QhauntzCombatComponent.h"
#include "QhauntzPlayerState.h" // We need this to get/set data
#include "Kismet/GameplayStatics.h" // Not used yet, but good to have

UQhauntzCombatComponent::UQhauntzCombatComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

void UQhauntzCombatComponent::BeginPlay()
{
	Super::BeginPlay();

	// Cache our owning PlayerState
	OwningPlayerState = Cast<AQhauntzPlayerState>(GetOwner());
    if (!OwningPlayerState)
    {
        UE_LOG(LogTemp, Error, TEXT("QhauntzCombatComponent: Could not find owning QhauntzPlayerState!"));
    }
}

// --- NEW FUNCTION IMPLEMENTATIONS ---

void UQhauntzCombatComponent::ApplyDamage(int32 DamageAmount, EStressType DamageType)
{
    if (!OwningPlayerState)
    {
        UE_LOG(LogTemp, Error, TEXT("ApplyDamage: No OwningPlayerState!"));
        return;
    }

    // --- RULE: Magical damage hits Resolve first. Physical hits Endurance first. ---
    // (We will implement this rule logic in a future script. For now, we
    // will use a simple Resolve -> Endurance -> Consequence overflow.)

    int32 DamageRemaining = DamageAmount;
    UE_LOG(LogTemp, Log, TEXT("ApplyDamage: Taking %d damage."), DamageRemaining);

    // --- Step 1: Try to absorb with Resolve Stress Track ---
    int32 ResolveBoxToFill = FindBestStressBox(OwningPlayerState->Resolve, DamageRemaining);
    if (ResolveBoxToFill > 0)
    {
        FillStressBox(OwningPlayerState->Resolve, ResolveBoxToFill);
        UE_LOG(LogTemp, Log, TEXT("ApplyDamage: Filled Resolve box [%d]. Damage absorbed."), ResolveBoxToFill);
        DamageRemaining = 0; // Damage is fully absorbed by one box
    }

    // --- Step 2: If damage remains, try to absorb with Endurance ---
    if (DamageRemaining > 0)
    {
        int32 EnduranceBoxToFill = FindBestStressBox(OwningPlayerState->Endurance, DamageRemaining);
        if (EnduranceBoxToFill > 0)
        {
            FillStressBox(OwningPlayerState->Endurance, EnduranceBoxToFill);
            UE_LOG(LogTemp, Log, TEXT("ApplyDamage: Filled Endurance box [%d]. Damage absorbed."), EnduranceBoxToFill);
            DamageRemaining = 0; // Damage is fully absorbed
        }
    }

    // --- Step 3: If damage *still* remains, try to take a Consequence ---
    if (DamageRemaining > 0)
    {
        UE_LOG(LogTemp, Log, TEXT("ApplyDamage: %d damage remains. Attempting to take Consequence..."), DamageRemaining);
        DamageRemaining = TakeConsequence(DamageRemaining, DamageType);
    }

    // --- Step 4: If damage *STILL* remains, character is Taken Out ---
    if (DamageRemaining > 0)
    {
        UE_LOG(LogTemp, Warning, TEXT("ApplyDamage: %d damage remains. No free Stress or Consequence slots. CHARACTER IS TAKEN OUT."), DamageRemaining);
        // TODO: Implement "Taken Out" logic
    }
}

int32 UQhauntzCombatComponent::FindBestStressBox(const FStressTrack& StressTrack, int32 DamageAmount)
{
    // --- RULE: "You can absorb a hit by checking one or more stress boxes..."
    // --- "...you can only check one box if the value of that box is
    // --- equal to or greater than the value of the hit."
    // We will find the *smallest* available box that is big enough.
    
    int32 BestBox = 0;
    for (int32 Box : StressTrack.Tracks)
    {
        // Check if this box is (A) big enough and (B) not already filled
        if (Box >= DamageAmount && !StressTrack.Filled.Contains(Box))
        {
            if (BestBox == 0 || Box < BestBox)
            {
                BestBox = Box; // Found a smaller, better-fitting box
            }
        }
    }
    return BestBox;
}

void UQhauntzCombatComponent::FillStressBox(UPARAM(ref) FStressTrack& StressTrack, int32 BoxValue)
{
    if (!StressTrack.Filled.Contains(BoxValue))
    {
        StressTrack.Filled.Add(BoxValue);
        // TODO: Here we would call a function to check for Aether track gains.
        CheckAetherTrackGains();
    }
}

int32 UQhauntzCombatComponent::TakeConsequence(int32 DamageAmount, EStressType DamageType)
{
    if (!OwningPlayerState) return DamageAmount;

    // --- RULE: Consequences absorb damage. Mild = 2, Moderate = 4, Severe = 6
    // We only have Mild slots right now, which absorb 2 damage.
    const int32 MildConsequenceValue = 2;

    // --- RULE: Try to use the matching Consequence type first ---
    // (This is a simplified version of the logic)

    if (DamageType == EStressType::EST_Resolve && OwningPlayerState->Consequences.Resolve_Mild.IsEmpty())
    {
        OwningPlayerState->Consequences.Resolve_Mild = TEXT("Default Mild Resolve Consequence");
        UE_LOG(LogTemp, Log, TEXT("TakeConsequence: Took Mild Resolve Consequence."));
        return DamageAmount - MildConsequenceValue;
    }
    
    if (DamageType == EStressType::EST_Endurance && OwningPlayerState->Consequences.Endurance_Mild.IsEmpty())
    {
        OwningPlayerState->Consequences.Endurance_Mild = TEXT("Default Mild Endurance Consequence");
        UE_LOG(LogTemp, Log, TEXT("TakeConsequence: Took Mild Endurance Consequence."));
        return DamageAmount - MildConsequenceValue;
    }
    
    if (OwningPlayerState->Consequences.Aether_Mild.IsEmpty())
    {
        OwningPlayerState->Consequences.Aether_Mild = TEXT("Default Mild Aether Consequence");
        UE_LOG(LogTemp, Log, TEXT("TakeConsequence: Took Mild Aether Consequence."));
        return DamageAmount - MildConsequenceValue;
    }

    // No free slots, return the full remaining damage
    UE_LOG(LogTemp, Warning, TEXT("TakeConsequence: No free Mild Consequence slots!"));
    return DamageAmount;
}


void UQhauntzCombatComponent::Tend(EStressType HealType, int32 HealShifts)
{
    if (!OwningPlayerState)
    {
        UE_LOG(LogTemp, Error, TEXT("Tend: No OwningPlayerState!"));
        return;
    }

    int32 HealShiftsRemaining = HealShifts;
    UE_LOG(LogTemp, Log, TEXT("Tend: Healing %d shifts of type %d."), HealShiftsRemaining, static_cast<int32>(HealType));

    // --- Step 1: Try to heal a Consequence first ---
    HealConsequence(HealType, HealShiftsRemaining);

    // --- Step 2: Use remaining shifts to heal Stress boxes ---
    if (HealShiftsRemaining > 0)
    {
        if (HealType == EStressType::EST_Endurance)
        {
            HealStressBox(OwningPlayerState->Endurance, HealShiftsRemaining);
        }
        else if (HealType == EStressType::EST_Resolve)
        {
            HealStressBox(OwningPlayerState->Resolve, HealShiftsRemaining);
        }
    }

    UE_LOG(LogTemp, Log, TEXT("Tend: Healing complete. %d shifts remaining."), HealShiftsRemaining);

    // After healing, we must re-check Aether gains
    // This is because removing filled boxes might reduce the total.
    CheckAetherTrackGains();
}


void UQhauntzCombatComponent::HealConsequence(EStressType HealType, int32& HealShiftsRemaining)
{
    if (!OwningPlayerState) return;

    // --- RULE: Healing a Mild Consequence costs 2 shifts ---
    const int32 MildConsequenceHealCost = 2;

    if (HealShiftsRemaining < MildConsequenceHealCost)
    {
        // Not enough shifts to heal a Consequence
        return;
    }

    // Check the matching Consequence type
    if (HealType == EStressType::EST_Endurance && !OwningPlayerState->Consequences.Endurance_Mild.IsEmpty())
    {
        OwningPlayerState->Consequences.Endurance_Mild.Empty();
        HealShiftsRemaining -= MildConsequenceHealCost;
        UE_LOG(LogTemp, Log, TEXT("HealConsequence: Cleared Mild Endurance Consequence."));
    }
    else if (HealType == EStressType::EST_Resolve && !OwningPlayerState->Consequences.Resolve_Mild.IsEmpty())
    {
        OwningPlayerState->Consequences.Resolve_Mild.Empty();
        HealShiftsRemaining -= MildConsequenceHealCost;
        UE_LOG(LogTemp, Log, TEXT("HealConsequence: Cleared Mild Resolve Consequence."));
    }
    // Note: We don't check Aether_Mild, as Tend() is only for Endurance/Resolve.
}


void UQhauntzCombatComponent::HealStressBox(UPARAM(ref) FStressTrack& StressTrack, int32& HealShiftsRemaining)
{
    if (StressTrack.Filled.Num() == 0)
    {
        // No boxes to heal
        return;
    }

    // --- RULE: Heal the *smallest* filled box first ---
    // We will loop as long as we have shifts and boxes to heal.

    bool bHealedAtLeastOneBox = true;
    while (bHealedAtLeastOneBox && HealShiftsRemaining > 0 && StressTrack.Filled.Num() > 0)
    {
        bHealedAtLeastOneBox = false; // Assume we won't find a box this loop

        // Find the smallest filled box
        int32 SmallestFilledBox = 0;
        int32 SmallestBoxIndex = -1;

        for (int32 i = 0; i < StressTrack.Filled.Num(); ++i)
        {
            int32 CurrentBox = StressTrack.Filled[i];
            if (SmallestBoxIndex == -1 || CurrentBox < SmallestFilledBox)
            {
                SmallestFilledBox = CurrentBox;
                SmallestBoxIndex = i;
            }
        }

        // Now check if we can afford to heal this box
        // --- RULE: HealShifts must be >= box value ---
        if (SmallestBoxIndex != -1 && HealShiftsRemaining >= SmallestFilledBox)
        {
            // Heal it!
            StressTrack.Filled.RemoveAt(SmallestBoxIndex);
            HealShiftsRemaining -= SmallestFilledBox;
            bHealedAtLeastOneBox = true; // We healed one, so we should loop again
            UE_LOG(LogTemp, Log, TEXT("HealStressBox: Cleared stress box [%d]."), SmallestFilledBox);
        }
    }
}

void UQhauntzCombatComponent::CheckAetherTrackGains()
{
    if (!OwningPlayerState) return;

    // --- RULE: If you have 3+ total stress filled, you get a temp Aether track ---
    const int32 TotalStress = OwningPlayerState->Endurance.Filled.Num() + OwningPlayerState->Resolve.Filled.Num();
    const int32 AetherGainThreshold = 3;
    const int32 TempAetherTrackValue = 1; // The temp track is always a '1'

    // Clear existing temp tracks first
    OwningPlayerState->Aether.Temp.Empty();

    if (TotalStress >= AetherGainThreshold)
    {
        OwningPlayerState->Aether.Temp.Add(TempAetherTrackValue);
        UE_LOG(LogTemp, Log, TEXT("CheckAetherTrackGains: Gained a temporary Aether track!"));
    }
}

