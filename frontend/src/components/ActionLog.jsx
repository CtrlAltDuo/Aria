import { useRef, useEffect } from 'react';

export default function ActionLog({ logs, isRunning }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const getActionColor = (action) => {
    const map = {
      click: 'bg-blue-500/20 text-blue-400',
      type: 'bg-emerald-500/20 text-emerald-400',
      scroll: 'bg-amber-500/20 text-amber-400',
      hotkey: 'bg-fuchsia-500/20 text-fuchsia-400',
      done: 'bg-success/20 text-success',
      fail: 'bg-error/20 text-error',
      wait: 'bg-muted/20 text-muted',
    };
    return map[action] || 'bg-muted/20 text-muted';
  };

  return (
    <div className="flex-1 overflow-y-auto bg-surface rounded-2xl border border-border p-4 shadow-sm">
      <div className="space-y-3">
        {logs.map((log, i) => (
          <div key={log.id || i} className="flex flex-col gap-1.5 p-3 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
            <div className="flex items-center justify-between">
              <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-md ${getActionColor(log.action_type)}`}>
                {log.action_type}
              </span>
              <span className="text-xs text-muted font-mono">
                {new Date(log.timestamp).toLocaleTimeString([], { hour12: false })}
              </span>
            </div>
            
            {log.reasoning && (
              <p className="text-sm text-text/90 leading-relaxed mt-1">
                {log.reasoning}
              </p>
            )}
            
            {log.confidence !== null && log.confidence !== undefined && (
              <div className="mt-2 text-xs text-muted flex items-center justify-end">
                Confidence: <span className="ml-1 font-mono">{(log.confidence * 100).toFixed(0)}%</span>
              </div>
            )}
          </div>
        ))}
        {logs.length === 0 && !isRunning && (
          <div className="text-center text-muted py-8 text-sm">
            No actions logged yet.
          </div>
        )}
        {isRunning && (
          <div className="flex items-center gap-3 p-4 rounded-xl bg-white/5 border border-white/5">
            <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
            <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse delay-75" />
            <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse delay-150" />
            <span className="text-xs text-muted ml-2 font-medium">Aria is thinking...</span>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
