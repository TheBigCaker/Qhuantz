
import React, { useMemo, useCallback } from 'react';
import { Character, SkillName, SkillRating, Status } from '../types';
import { ALL_SKILLS, MAGICAL_SKILLS, NON_MAGICAL_SKILLS, SKILL_PYRAMID_SLOTS, STATUS_OPTIONS, STATUS_DESCRIPTIONS } from '../constants';
import Card, { CardContent, CardHeader } from './ui/Card';
import Input from './ui/Input';
import Select from './ui/Select';
import Button from './ui/Button';
import { Trash2 } from 'lucide-react';

interface CharacterSheetProps {
  character: Character;
  setCharacter: React.Dispatch<React.SetStateAction<Character>>;
}

const CharacterSheet: React.FC<CharacterSheetProps> = ({ character, setCharacter }) => {

  const handleInputChange = (field: keyof Character, value: any) => {
    setCharacter(prev => ({ ...prev, [field]: value }));
  };

  const handleAspectChange = (field: 'maxim' | 'imperative' | 'guild' | 'name', value: string) => {
    setCharacter(prev => ({ ...prev, [field]: value }));
  };

  const handleAffinityChange = (field: keyof Character['affinity'], value: string) => {
    setCharacter(prev => ({ ...prev, affinity: { ...prev.affinity, [field]: value } }));
  };

  const handleSkillChange = (skillName: SkillName, rating: SkillRating) => {
    setCharacter(prev => ({ ...prev, skills: { ...prev.skills, [skillName]: rating } }));
  };

  const handleStuntChange = (index: number, value: string) => {
    const newStunts = [...character.stunts];
    newStunts[index] = value;
    setCharacter(prev => ({ ...prev, stunts: newStunts }));
  };
  
  const addStunt = () => setCharacter(prev => ({ ...prev, stunts: [...prev.stunts, ''] }));
  const removeStunt = (index: number) => setCharacter(prev => ({ ...prev, stunts: prev.stunts.filter((_, i) => i !== index) }));

  const skillPoints = useMemo(() => Object.values(character.skills).reduce((a, b) => a + b, 0), [character.skills]);
  const magicalSkillPoints = useMemo(() => MAGICAL_SKILLS.reduce((sum, skill) => sum + character.skills[skill], 0), [character.skills]);

  const aetherTracks = useMemo(() => {
    const tracks = [];
    let remainingPoints = magicalSkillPoints;
    for (let i = 1; i <= 10; i++) {
      remainingPoints -= i;
      if (remainingPoints >= 0) {
        tracks.push(i);
      } else {
        break;
      }
    }
    return tracks;
  }, [magicalSkillPoints]);

  const enduranceBoxes = useMemo(() => {
    const physique = character.skills.Physique;
    let bonus = 0;
    if (physique >= 1) bonus = 1;
    if (physique >= 3) bonus = 2;
    if (physique >= 5) bonus = 3; // Assuming progression
    return 2 + bonus;
  }, [character.skills.Physique]);

  const resolveBoxes = useMemo(() => {
    const will = character.skills.Will;
    let bonus = 0;
    if (will >= 1) bonus = 1;
    if (will >= 3) bonus = 2;
    if (will >= 5) bonus = 3; // Assuming progression
    return 2 + bonus;
  }, [character.skills.Will]);

  const renderSkillPyramid = useCallback(() => {
    const ratings = [4, 3, 2, 1] as const;
    const skillCounts = Object.values(character.skills).reduce((acc, rating) => {
        if (rating > 0) acc[rating] = (acc[rating] || 0) + 1;
        return acc;
    }, {} as Record<SkillRating, number>);

    return ratings.map(rating => (
        <div key={rating} className="mb-4">
            <h4 className="font-bold text-slate-300 mb-2">
                {rating === 4 ? 'Great (+4)' : rating === 3 ? 'Good (+3)' : rating === 2 ? 'Fair (+2)' : 'Average (+1)'}
                <span className="ml-2 text-sm font-normal text-slate-400">
                    ({skillCounts[rating] || 0} / {SKILL_PYRAMID_SLOTS[rating]})
                </span>
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                {Array.from({ length: SKILL_PYRAMID_SLOTS[rating] }).map((_, i) => {
                    const assignedSkill = Object.entries(character.skills).find(([_, r]) => r === rating);
                    const currentSkillForSlot = Object.keys(character.skills).filter(s => character.skills[s as SkillName] === rating)[i];
                    
                    return (
                        <Select
                            key={i}
                            value={currentSkillForSlot || ''}
                            onChange={(e) => {
                                const newSkill = e.target.value as SkillName;
                                const oldSkill = currentSkillForSlot as SkillName;
                                setCharacter(prev => {
                                    const newSkills = { ...prev.skills };
                                    if (oldSkill) newSkills[oldSkill] = 0;
                                    if (newSkill) newSkills[newSkill] = rating as SkillRating;
                                    return { ...prev, skills: newSkills };
                                });
                            }}
                        >
                            <option value="">- Select Skill -</option>
                            {ALL_SKILLS.map(skill => (
                                <option key={skill} value={skill} disabled={character.skills[skill] > 0 && character.skills[skill] !== rating}>
                                    {skill}
                                </option>
                            ))}
                        </Select>
                    );
                })}
            </div>
        </div>
    ));
  }, [character.skills, setCharacter]);

  const StressTrack = ({ label, total, type }: { label: string, total: number, type: 'endurance' | 'resolve' }) => (
    <div>
        <h4 className="font-bold text-slate-300 mb-2">{label} ({total} boxes)</h4>
        <div className="flex flex-wrap gap-2">
            {Array.from({ length: total }).map((_, i) => (
                <div key={i} className="w-8 h-8 border-2 border-slate-600 rounded flex items-center justify-center bg-slate-900">
                    {i + 1}
                </div>
            ))}
        </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>Core Identity</CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input label="Name" value={character.name} onChange={e => handleAspectChange('name', e.target.value)} />
          <Input label="Maxim (High Concept)" value={character.maxim} onChange={e => handleAspectChange('maxim', e.target.value)} />
          <Input label="Imperative (Trouble)" value={character.imperative} onChange={e => handleAspectChange('imperative', e.target.value)} />
          <Input label="Guild" value={character.guild} onChange={e => handleAspectChange('guild', e.target.value)} />
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
            <Card>
                <CardHeader>Skills</CardHeader>
                <CardContent>
                    {renderSkillPyramid()}
                    <div className="mt-4 pt-4 border-t border-slate-700/50">
                        <h4 className="font-bold text-slate-300 mb-2">Mediocre (+0) Skills</h4>
                        <p className="text-slate-400 text-sm">
                            {ALL_SKILLS.filter(s => character.skills[s] === 0).join(', ')}
                        </p>
                    </div>
                </CardContent>
            </Card>
            <Card>
                <CardHeader>Stunts & Runes</CardHeader>
                <CardContent className="space-y-3">
                    {character.stunts.map((stunt, index) => (
                        <div key={index} className="flex items-center gap-2">
                            <Input
                                aria-label={`Stunt ${index + 1}`}
                                value={stunt}
                                onChange={e => handleStuntChange(index, e.target.value)}
                                className="flex-grow"
                            />
                            <Button variant="ghost" size="sm" onClick={() => removeStunt(index)} aria-label={`Remove Stunt ${index + 1}`}>
                                <Trash2 size={16} />
                            </Button>
                        </div>
                    ))}
                    <Button onClick={addStunt} variant="secondary" size="sm">Add Stunt</Button>
                </CardContent>
            </Card>
        </div>

        <div className="space-y-6">
            <Card>
                <CardHeader>Status</CardHeader>
                <CardContent>
                    <Select label="Select Status" value={character.status} onChange={e => handleInputChange('status', e.target.value as Status)}>
                        {STATUS_OPTIONS.map(s => <option key={s} value={s}>{s}</option>)}
                    </Select>
                    <div className="mt-3 text-sm text-slate-400">
                        <p><strong className="text-slate-300">({STATUS_DESCRIPTIONS[character.status].pronunciation})</strong> {STATUS_DESCRIPTIONS[character.status].core}</p>
                    </div>
                </CardContent>
            </Card>
            <Card>
                <CardHeader>Affinity</CardHeader>
                <CardContent className="space-y-3">
                    <Input label="Affinity Name" value={character.affinity.name} onChange={e => handleAffinityChange('name', e.target.value)} />
                    <Select label="Attack Skill" value={character.affinity.attack} onChange={e => handleAffinityChange('attack', e.target.value as SkillName)}>
                        <option value="">- Select -</option>
                        {MAGICAL_SKILLS.map(s => <option key={s} value={s}>{s}</option>)}
                    </Select>
                    <Select label="Defend Skill" value={character.affinity.defend} onChange={e => handleAffinityChange('defend', e.target.value as SkillName)}>
                        <option value="">- Select -</option>
                        {MAGICAL_SKILLS.map(s => <option key={s} value={s}>{s}</option>)}
                    </Select>
                    <Select label="Tend Skill" value={character.affinity.tend} onChange={e => handleAffinityChange('tend', e.target.value as SkillName)}>
                        <option value="">- Select -</option>
                        {MAGICAL_SKILLS.map(s => <option key={s} value={s}>{s}</option>)}
                    </Select>
                    <Select label="Non-Combat Skill" value={character.affinity.nonCombat} onChange={e => handleAffinityChange('nonCombat', e.target.value as SkillName)}>
                        <option value="">- Select -</option>
                        {MAGICAL_SKILLS.map(s => <option key={s} value={s}>{s}</option>)}
                    </Select>
                </CardContent>
            </Card>
            <Card>
                <CardHeader>Tracks & Pools</CardHeader>
                <CardContent className="space-y-4">
                    <StressTrack label="Endurance" total={enduranceBoxes} type="endurance" />
                    <StressTrack label="Resolve" total={resolveBoxes} type="resolve" />
                    <div>
                        <h4 className="font-bold text-slate-300 mb-2">Aether Pool</h4>
                        <div className="flex flex-wrap gap-2">
                            {aetherTracks.length > 0 ? aetherTracks.map(track => (
                                <div key={track} className="w-8 h-8 border-2 border-cyan-400 rounded flex items-center justify-center bg-cyan-900/50 text-cyan-300 font-bold">
                                    {track}
                                </div>
                            )) : <p className="text-sm text-slate-400">No Aether tracks. Increase magical skills.</p>}
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
      </div>
    </div>
  );
};

export default CharacterSheet;
