
import React, { useState, useRef, useEffect } from 'react';
import { Bot, Loader, Send, Sparkles, User } from 'lucide-react';
import Card, { CardContent } from './ui/Card';
import Button from './ui/Button';
import { useGeminiStream } from '../hooks/useGeminiStream';
import { Message } from '../types';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const ChatMessage: React.FC<{ message: Message }> = ({ message }) => {
  const isModel = message.role === 'model';
  return (
    <div className={`flex items-start gap-4 ${isModel ? '' : 'justify-end'}`}>
      {isModel && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-violet-500 flex items-center justify-center text-white">
          <Bot size={20} />
        </div>
      )}
      <div className={`max-w-xl w-fit px-4 py-3 rounded-lg ${isModel ? 'bg-slate-700/50' : 'bg-blue-600 text-white'}`}>
        <div className="prose prose-sm prose-invert max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.text}</ReactMarkdown>
        </div>
        {message.isStreaming && <span className="inline-block w-2 h-4 bg-white animate-pulse ml-1" />}
      </div>
      {!isModel && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-slate-600 flex items-center justify-center text-white">
          <User size={20} />
        </div>
      )}
    </div>
  );
};

const GmAssist: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const { messages, sendMessage, isLoading, error } = useGeminiStream();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || isLoading) return;
    sendMessage(prompt);
    setPrompt('');
  };

  const handlePresetPrompt = (preset: string) => {
    if (isLoading) return;
    sendMessage(preset);
  };

  const presetPrompts = [
    "Describe a bustling market in a Fyemyn city.",
    "Create a Tyrmyn engineer NPC with a problematic secret.",
    "A magical experiment goes wrong. What happens?",
    "Generate three interesting plot hooks for a new campaign.",
  ];

  return (
    <Card className="flex flex-col h-[calc(100vh-10rem)] md:h-[calc(100vh-12rem)]">
      <div className="flex-grow p-4 overflow-y-auto space-y-6">
        {messages.length === 0 && (
          <div className="text-center text-slate-400 flex flex-col items-center justify-center h-full">
            <Sparkles size={48} className="mb-4 text-violet-400" />
            <h2 className="text-2xl font-bold text-white mb-2 font-orbitron">GM Assistant</h2>
            <p>What story can I help you create today?</p>
            <div className="mt-6 w-full max-w-md grid grid-cols-1 sm:grid-cols-2 gap-2">
              {presetPrompts.map((p, i) => (
                <Button key={i} variant="secondary" size="sm" onClick={() => handlePresetPrompt(p)} disabled={isLoading}>
                  {p}
                </Button>
              ))}
            </div>
          </div>
        )}
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}
        {isLoading && messages.length > 0 && (
          <div className="flex items-center gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-violet-500 flex items-center justify-center text-white">
              <Loader size={20} className="animate-spin" />
            </div>
            <div className="max-w-xl w-fit px-4 py-3 rounded-lg bg-slate-700/50">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
              </div>
            </div>
          </div>
        )}
        {error && <div className="text-red-400 text-center">{error}</div>}
        <div ref={messagesEndRef} />
      </div>
      <div className="p-4 border-t border-slate-700/50">
        <form onSubmit={handleSubmit} className="flex items-center gap-2">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Ask Gemini to generate a scene, NPC, or plot twist..."
            className="flex-grow bg-slate-900/50 border border-slate-600 rounded-md px-4 py-2 text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-violet-500"
            disabled={isLoading}
            aria-label="GM prompt input"
          />
          <Button type="submit" disabled={isLoading || !prompt.trim()} aria-label="Send prompt">
            <Send size={18} />
          </Button>
        </form>
      </div>
    </Card>
  );
};

export default GmAssist;
