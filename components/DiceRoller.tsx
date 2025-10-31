
import React, { useState, useMemo } from 'react';
import { Dices } from 'lucide-react';
import Card, { CardContent, CardHeader } from './ui/Card';
import Button from './ui/Button';
import { FateDiceRoll, DiceValue } from '../types';
import { PlusIcon, MinusIcon, BlankIcon } from './icons';

const DiceIcon: React.FC<{ value: DiceValue }> = ({ value }) => {
  const baseClasses = "w-12 h-12 md:w-16 md:h-16 flex items-center justify-center rounded-lg border-2";
  const colorClasses = {
    '1': 'border-green-400 text-green-400 bg-green-900/30',
    '-1': 'border-red-400 text-red-400 bg-red-900/30',
    '0': 'border-slate-500 text-slate-500 bg-slate-800/30',
  };

  return (
    <div className={`${baseClasses} ${colorClasses[value]}`}>
      {value === 1 && <PlusIcon />}
      {value === -1 && <MinusIcon />}
      {value === 0 && <BlankIcon />}
    </div>
  );
};

const DiceRoller: React.FC = () => {
  const [roll, setRoll] = useState<FateDiceRoll | null>(null);
  const [isRolling, setIsRolling] = useState(false);

  const total = useMemo(() => {
    if (!roll) return 0;
    return roll.reduce((sum, val) => sum + val, 0);
  }, [roll]);

  const rollDice = () => {
    setIsRolling(true);
    setRoll(null);

    setTimeout(() => {
      const newRoll = Array.from({ length: 4 }, () => {
        const r = Math.floor(Math.random() * 3) - 1;
        return r as DiceValue;
      }) as FateDiceRoll;
      setRoll(newRoll);
      setIsRolling(false);
    }, 500); // Animation duration
  };

  return (
    <div className="max-w-2xl mx-auto">
      <Card>
        <CardHeader>Fate Dice Roller</CardHeader>
        <CardContent className="flex flex-col items-center gap-8">
          <div className="w-full h-24 flex items-center justify-center">
            {isRolling && <Dices size={64} className="animate-spin text-violet-400" />}
            {!isRolling && roll && (
              <div className="flex flex-col items-center gap-4 animate-fade-in">
                <div className="flex gap-4">
                  {roll.map((value, index) => (
                    <DiceIcon key={index} value={value} />
                  ))}
                </div>
              </div>
            )}
            {!isRolling && !roll && (
              <p className="text-slate-400">Click the button to roll the dice.</p>
            )}
          </div>

          {!isRolling && roll && (
            <div className="text-center animate-fade-in">
              <p className="text-lg text-slate-300">Total Result</p>
              <p className="text-6xl font-bold font-orbitron" style={{ color: total > 0 ? '#6ee7b7' : total < 0 ? '#f87171' : '#94a3b8' }}>
                {total > 0 ? `+${total}` : total}
              </p>
            </div>
          )}

          <Button onClick={rollDice} disabled={isRolling} size="lg">
            <Dices size={20} className="mr-2" />
            {isRolling ? 'Rolling...' : 'Roll 4dF'}
          </Button>
        </CardContent>
      </Card>
      <style>{`
        @keyframes fade-in {
          from { opacity: 0; transform: scale(0.9); }
          to { opacity: 1; transform: scale(1); }
        }
        .animate-fade-in {
          animation: fade-in 0.3s ease-out forwards;
        }
      `}</style>
    </div>
  );
};

export default DiceRoller;
