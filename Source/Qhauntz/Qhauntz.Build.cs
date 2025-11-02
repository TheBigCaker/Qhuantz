
// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class Qhauntz : ModuleRules
{
	public Qhauntz(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
	
        // --- MODIFIED: Added GameplayAbilities, GameplayTags, GameplayTasks ---
		PublicDependencyModuleNames.AddRange(new string[] 
        { 
            "Core", 
            "CoreUObject", 
            "Engine", 
            "InputCore",
            "GameplayAbilities", // Added for future magic system
            "GameplayTags",      // Added for future magic system
            "GameplayTasks"      // Added for future magic system
        });

		PrivateDependencyModuleNames.AddRange(new string[] {  });

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });
		
		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
