
import React, { useState, useMemo } from 'react';
import Card, { CardContent } from './ui/Card';
import Input from './ui/Input';
import { rulesMarkdown } from '../lib/rules';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Search } from 'lucide-react';

const RulesExplorer: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredRules = useMemo(() => {
    if (!searchTerm.trim()) {
      return rulesMarkdown;
    }
    const lowerCaseSearch = searchTerm.toLowerCase();
    // This is a simple filter. It will show the whole text if any part matches.
    // A more advanced implementation might split the markdown into sections.
    return rulesMarkdown.toLowerCase().includes(lowerCaseSearch) ? rulesMarkdown : "No matching rules found.";
  }, [searchTerm]);

  return (
    <div className="space-y-4">
      <div className="relative">
        <Input
          type="text"
          placeholder="Search rules..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="pl-10"
          aria-label="Search rules"
        />
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
      </div>
      <Card>
        <CardContent>
          <article className="prose prose-slate prose-invert max-w-none 
            prose-headings:font-orbitron prose-headings:text-violet-300
            prose-h1:text-3xl prose-h2:text-2xl prose-h3:text-xl
            prose-a:text-cyan-400 hover:prose-a:text-cyan-300
            prose-strong:text-slate-100
            prose-code:bg-slate-900 prose-code:p-1 prose-code:rounded
            prose-blockquote:border-l-violet-400 prose-blockquote:text-slate-400
            prose-table:border-slate-700 prose-th:bg-slate-900/50 prose-tr:border-slate-700">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {filteredRules}
            </ReactMarkdown>
          </article>
        </CardContent>
      </Card>
    </div>
  );
};

export default RulesExplorer;
