import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Send, Sparkles } from 'lucide-react';

export default function NewTask() {
  const [instruction, setInstruction] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!instruction.trim()) return;
    
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/tasks', { instruction });
      navigate(`/task/${res.data.id}`);
    } catch (error) {
      console.error('Failed to create task', error);
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-3xl mx-auto h-full flex flex-col justify-center">
      <div className="mb-8 flex items-center gap-3">
        <div className="p-3 bg-accent/20 text-accent rounded-xl border border-accent/20">
          <Sparkles size={24} />
        </div>
        <div>
          <h2 className="text-3xl font-bold">Give Aria a task</h2>
          <p className="text-muted mt-1">Describe what you want to automate in plain English.</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="relative group">
        <div className="absolute -inset-0.5 bg-gradient-to-r from-accent to-fuchsia-600 rounded-2xl blur opacity-20 group-focus-within:opacity-40 transition duration-500"></div>
        <div className="relative bg-surface border border-border rounded-2xl flex flex-col shadow-xl">
          <textarea
            value={instruction}
            onChange={(e) => setInstruction(e.target.value)}
            placeholder="e.g. Open Salesforce, find John Smith, update his notes with: Interested in senior roles, available in 60 days"
            className="w-full h-48 bg-transparent text-text p-6 resize-none focus:outline-none placeholder:text-muted/60 text-lg leading-relaxed"
            autoFocus
          />
          <div className="p-4 border-t border-border flex justify-between items-center bg-white/5 rounded-b-2xl">
            <span className="text-xs text-muted flex items-center gap-1.5">
              Press <kbd className="px-2 py-1 bg-background border border-border rounded-md font-sans">Cmd</kbd> + <kbd className="px-2 py-1 bg-background border border-border rounded-md font-sans">Enter</kbd> to submit
            </span>
            <button
              type="submit"
              disabled={loading || !instruction.trim()}
              className="bg-accent hover:bg-accent/90 disabled:opacity-50 disabled:hover:bg-accent text-white px-6 py-2.5 rounded-xl font-medium flex items-center gap-2 transition-all hover:scale-[1.02] active:scale-[0.98]"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  Start Task <Send size={16} />
                </>
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
