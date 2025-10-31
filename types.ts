
export type SkillName = 
  | 'Analysis' | 'Compel' | 'Conjuration' | 'Empathy' | 'Enhancement' | 'Illusion' 
  | 'Mysticism' | 'Perception' | 'Suppression' | 'Telekinesis' | 'Teleportation' | 'Will'
  | 'Engineering' | 'Marksmanship' | 'Martial Arts' | 'Physique';

export type SkillRating = 0 | 1 | 2 | 3 | 4;

export type Skill = {
  name: SkillName;
  rating: SkillRating;
};

export type Status = 'Fyemyn' | 'Ayrmyn' | 'Tyrmyn' | 'Fyrmyn' | 'Ayxmyn' | 'Nyhmyn';

export type Affinity = {
  name: string;
  attack: SkillName | '';
  defend: SkillName | '';
  tend: SkillName | '';
  nonCombat: SkillName | '';
};

export type Character = {
  name: string;
  maxim: string;
  imperative: string;
  guild: string;
  status: Status;
  affinity: Affinity;
  skills: Record<SkillName, SkillRating>;
  stunts: string[];
  stress: {
    endurance: number[];
    resolve: number[];
  };
  consequences: {
    endurance: { value: 2 | 4 | 6; description: string }[];
    resolve: { value: 2 | 4 | 6; description: string }[];
  };
};

export type DiceValue = -1 | 0 | 1;
export type FateDiceRoll = [DiceValue, DiceValue, DiceValue, DiceValue];

export interface Message {
  id: string;
  role: 'user' | 'model';
  text: string;
  isStreaming?: boolean;
}
