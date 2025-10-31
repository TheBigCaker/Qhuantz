
import React, { useState, useMemo } from 'react';
import { Tabs, Tab } from './components/ui/Tabs';
import CharacterSheet from './components/CharacterSheet';
import GmAssist from './components/GmAssist';
import DiceRoller from './components/DiceRoller';
import RulesExplorer from './components/RulesExplorer';
import { BookOpen, BotMessageSquare, Dices, UserSquare } from 'lucide-react';
import { Character } from './types';
import { BLANK_CHARACTER } from './constants';

type TabId = 'character' | 'gm' | 'dice' | 'rules';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabId>('character');
  const [character, setCharacter] = useState<Character>(BLANK_CHARACTER);

  const tabs: Tab<TabId>[] = useMemo(() => [
    { id: 'character', label: 'Character', icon: <UserSquare size={18} /> },
    { id: 'gm', label: 'GM Assist', icon: <BotMessageSquare size={18} /> },
    { id: 'dice', label: 'Dice Roller', icon: <Dices size={18} /> },
    { id: 'rules', label: 'Rules', icon: <BookOpen size={18} /> },
  ], []);

  const renderContent = () => {
    switch (activeTab) {
      case 'character':
        return <CharacterSheet character={character} setCharacter={setCharacter} />;
      case 'gm':
        return <GmAssist />;
      case 'dice':
        return <DiceRoller />;
      case 'rules':
        return <RulesExplorer />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-200 flex flex-col">
      <header className="bg-slate-950/50 backdrop-blur-sm border-b border-slate-700/50 sticky top-0 z-20">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center">
          <h1 className="text-xl md:text-2xl font-bold text-white tracking-wider">
            <span className="text-violet-400">Qhauntz</span> AI Toolkit
          </h1>
          <div className="hidden md:block">
            <Tabs tabs={tabs} activeTab={activeTab} onTabClick={setActiveTab} />
          </div>
        </div>
      </header>

      <main className="flex-grow container mx-auto p-4 md:p-6">
        {renderContent()}
      </main>

      <footer className="md:hidden fixed bottom-0 left-0 right-0 bg-slate-950/80 backdrop-blur-sm border-t border-slate-700/50 z-20">
        <Tabs tabs={tabs} activeTab={activeTab} onTabClick={setActiveTab} isMobile />
      </footer>
      <div className="md:hidden h-20"></div> {/* Spacer for mobile footer */}
    </div>
  );
};

export default App;
