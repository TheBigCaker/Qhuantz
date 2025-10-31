
import { Character, SkillName, Status } from './types';

export const MAGICAL_SKILLS: SkillName[] = [
  'Analysis', 'Compel', 'Conjuration', 'Empathy', 'Enhancement', 'Illusion', 
  'Mysticism', 'Perception', 'Suppression', 'Telekinesis', 'Teleportation', 'Will'
];

export const NON_MAGICAL_SKILLS: SkillName[] = [
  'Engineering', 'Marksmanship', 'Martial Arts', 'Physique'
];

export const ALL_SKILLS: SkillName[] = [...MAGICAL_SKILLS, ...NON_MAGICAL_SKILLS];

export const STATUS_OPTIONS: Status[] = ['Fyemyn', 'Ayrmyn', 'Tyrmyn', 'Fyrmyn', 'Ayxmyn', 'Nyhmyn'];

export const SKILL_PYRAMID_SLOTS = { 4: 1, 3: 2, 2: 3, 1: 4 };

export const BLANK_CHARACTER: Character = {
  name: '',
  maxim: '',
  imperative: '',
  guild: '',
  status: 'Fyemyn',
  affinity: {
    name: '',
    attack: '',
    defend: '',
    tend: '',
    nonCombat: '',
  },
  skills: ALL_SKILLS.reduce((acc, skill) => {
    acc[skill] = 0;
    return acc;
  }, {} as Record<SkillName, 0>),
  stunts: ['', ''],
  stress: {
    endurance: [],
    resolve: [],
  },
  consequences: {
    endurance: [],
    resolve: [],
  },
};

export const STATUS_DESCRIPTIONS: Record<Status, { core: string, pronunciation: string }> = {
    Fyemyn: { pronunciation: "Fay-men", core: "Pure Mage. Regenerates an additional lower Aether track each turn. Can use magic outside Affinity with a -1 penalty." },
    Ayrmyn: { pronunciation: "Air-men", core: "Rune Golem. Gains +1 Resolve and +1 Aether track per Rune Stunt." },
    Tyrmyn: { pronunciation: "Tear-men", core: "Rune User. Can use magic outside Affinity with a -1 penalty." },
    Fyrmyn: { pronunciation: "Fear-men", core: "Restricted Rune User. Magical weapon actions costing 1-2 Aether are free. Cannot use magic outside their Affinity." },
    Ayxmyn: { pronunciation: "X-men", core: "Pacified Rune User. Gains +1 Endurance and +1 Resolve track per Rune Stunt. Can only use skills from their Affinity." },
    Nyhmyn: { pronunciation: "Nigh-men", core: "Magic Sponge/Tank. Absorbs magical energy to fuel physical prowess. See special rules." },
};
