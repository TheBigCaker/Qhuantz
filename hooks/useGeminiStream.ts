
import { useState } from 'react';
import { generateContentStream } from '../lib/gemini';
import { Message } from '../types';

export const useGeminiStream = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (prompt: string) => {
    setIsLoading(true);
    setError(null);

    const userMessage: Message = { id: Date.now().toString(), role: 'user', text: prompt };
    setMessages(prev => [...prev, userMessage]);

    const modelMessageId = (Date.now() + 1).toString();
    
    try {
      const stream = await generateContentStream(prompt);
      
      setMessages(prev => [...prev, { id: modelMessageId, role: 'model', text: '', isStreaming: true }]);

      for await (const chunk of stream) {
        const chunkText = chunk.text;
        setMessages(prev =>
          prev.map(msg =>
            msg.id === modelMessageId
              ? { ...msg, text: msg.text + chunkText }
              : msg
          )
        );
      }

      setMessages(prev =>
        prev.map(msg =>
          msg.id === modelMessageId
            ? { ...msg, isStreaming: false }
            : msg
        )
      );

    } catch (e) {
      console.error(e);
      const errorMessage = e instanceof Error ? e.message : 'An unknown error occurred.';
      setError(`Error generating response: ${errorMessage}`);
      setMessages(prev => prev.filter(msg => msg.id !== modelMessageId));
    } finally {
      setIsLoading(false);
    }
  };

  return { messages, sendMessage, isLoading, error };
};
