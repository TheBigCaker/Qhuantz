
import React from 'react';

export interface Tab<T extends string> {
  id: T;
  label: string;
  icon?: React.ReactNode;
}

interface TabsProps<T extends string> {
  tabs: Tab<T>[];
  activeTab: T;
  onTabClick: (id: T) => void;
  isMobile?: boolean;
}

export function Tabs<T extends string>({ tabs, activeTab, onTabClick, isMobile = false }: TabsProps<T>) {
  if (isMobile) {
    return (
      <nav className="grid grid-cols-4 gap-1 p-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabClick(tab.id)}
            className={`flex flex-col items-center justify-center p-2 rounded-lg transition-colors duration-200 ${
              activeTab === tab.id
                ? 'bg-violet-600 text-white'
                : 'text-slate-400 hover:bg-slate-700/50 hover:text-white'
            }`}
            aria-current={activeTab === tab.id ? 'page' : undefined}
          >
            {tab.icon}
            <span className="text-xs mt-1">{tab.label}</span>
          </button>
        ))}
      </nav>
    );
  }

  return (
    <nav className="flex space-x-2 bg-slate-800/50 p-1 rounded-lg">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onTabClick(tab.id)}
          className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
            activeTab === tab.id
              ? 'bg-violet-600 text-white shadow-md'
              : 'text-slate-300 hover:bg-slate-700/50 hover:text-white'
          }`}
          aria-current={activeTab === tab.id ? 'page' : undefined}
        >
          {tab.icon}
          <span>{tab.label}</span>
        </button>
      ))}
    </nav>
  );
}
