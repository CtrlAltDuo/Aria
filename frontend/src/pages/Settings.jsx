import { useState, useEffect } from 'react';
import axios from 'axios';
import { Save, Key, Globe, Cpu } from 'lucide-react';

export default function Settings() {
  const [settings, setSettings] = useState({
    GEMINI_API_KEY: '',
    OLLAMA_URL: 'http://localhost:11434',
    AI_PROVIDER: 'auto'
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const res = await axios.get('http://localhost:8000/settings');
        setSettings({
          GEMINI_API_KEY: res.data.GEMINI_API_KEY || '',
          OLLAMA_URL: res.data.OLLAMA_URL || 'http://localhost:11434',
          AI_PROVIDER: res.data.AI_PROVIDER || 'auto'
        });
      } catch (error) {
        console.error('Failed to fetch settings', error);
      }
    };
    fetchSettings();
  }, []);

  const handleChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage('');
    try {
      for (const [key, value] of Object.entries(settings)) {
        await axios.put('http://localhost:8000/settings', { key, value });
      }
      setMessage('Settings saved successfully!');
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Failed to save settings.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="p-8 max-w-3xl mx-auto space-y-8">
      <header>
        <h2 className="text-3xl font-bold mb-2">Settings</h2>
        <p className="text-muted">Configure your AI providers and preferences</p>
      </header>

      <div className="bg-surface border border-border rounded-2xl overflow-hidden shadow-sm">
        <div className="p-6 space-y-8">
          
          <div className="space-y-4">
            <div className="flex items-center gap-2 border-b border-border pb-2">
              <Cpu className="text-accent" size={20} />
              <h3 className="font-semibold text-lg">AI Provider</h3>
            </div>
            <div className="flex gap-4">
              {['auto', 'gemini', 'ollama'].map((provider) => (
                <label key={provider} className={`flex-1 cursor-pointer border rounded-xl p-4 flex items-center justify-center gap-3 transition-colors ${
                  settings.AI_PROVIDER === provider 
                    ? 'border-accent bg-accent/10 text-accent font-medium' 
                    : 'border-border hover:border-muted/50 bg-white/5'
                }`}>
                  <input
                    type="radio"
                    name="provider"
                    value={provider}
                    checked={settings.AI_PROVIDER === provider}
                    onChange={() => handleChange('AI_PROVIDER', provider)}
                    className="sr-only"
                  />
                  <span className="capitalize">{provider}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-2 border-b border-border pb-2">
              <Key className="text-blue-500" size={20} />
              <h3 className="font-semibold text-lg">Google Gemini</h3>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-muted block">API Key</label>
              <input
                type="password"
                value={settings.GEMINI_API_KEY}
                onChange={(e) => handleChange('GEMINI_API_KEY', e.target.value)}
                placeholder="AIzaSy..."
                className="w-full bg-background border border-border rounded-xl px-4 py-3 focus:outline-none focus:border-accent transition-colors"
              />
              <p className="text-xs text-muted mt-2">
                Get a free Gemini key at <a href="https://aistudio.google.com" target="_blank" rel="noreferrer" className="text-accent hover:underline">aistudio.google.com</a>
              </p>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-2 border-b border-border pb-2">
              <Globe className="text-emerald-500" size={20} />
              <h3 className="font-semibold text-lg">Ollama (Local)</h3>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-muted block">Host URL</label>
              <input
                type="text"
                value={settings.OLLAMA_URL}
                onChange={(e) => handleChange('OLLAMA_URL', e.target.value)}
                placeholder="http://localhost:11434"
                className="w-full bg-background border border-border rounded-xl px-4 py-3 focus:outline-none focus:border-accent transition-colors"
              />
            </div>
          </div>

        </div>
        
        <div className="p-6 border-t border-border bg-white/5 flex items-center justify-between">
          <div className="text-sm">
            {message && (
              <span className={message.includes('success') ? 'text-success' : 'text-error'}>
                {message}
              </span>
            )}
          </div>
          <button
            onClick={handleSave}
            disabled={saving}
            className="bg-accent hover:bg-accent/90 disabled:opacity-50 text-white px-6 py-2.5 rounded-xl font-medium flex items-center gap-2 transition-all hover:scale-[1.02] active:scale-[0.98]"
          >
            {saving ? 'Saving...' : (
              <>
                <Save size={18} /> Save Settings
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
