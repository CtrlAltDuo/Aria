import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import StatusBadge from '../components/StatusBadge';
import ActionLog from '../components/ActionLog';
import { AlertCircle, CheckCircle2 } from 'lucide-react';

export default function TaskDetail() {
  const { id } = useParams();
  const [task, setTask] = useState(null);
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    // Initial fetch
    const fetchTask = async () => {
      try {
        const res = await axios.get(`http://localhost:8000/tasks/${id}`);
        setTask(res.data);
        setLogs(res.data.logs);
      } catch (error) {
        console.error('Failed to fetch task', error);
      }
    };
    fetchTask();

    // Setup WebSocket
    const ws = new WebSocket(`ws://localhost:8000/ws/${id}`);
    
    ws.onmessage = (event) => {
      const log = JSON.parse(event.data);
      setLogs((prev) => [...prev, log]);
      
      // Also refetch task to update status when a new log arrives
      // (a slightly hacky way to keep status in sync, but effective)
      axios.get(`http://localhost:8000/tasks/${id}`).then(res => {
        setTask(res.data);
      });
    };

    return () => {
      ws.close();
    };
  }, [id]);

  if (!task) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-accent/30 border-t-accent rounded-full animate-spin" />
      </div>
    );
  }

  const isRunning = task.status === 'running' || task.status === 'pending';

  return (
    <div className="p-8 max-w-5xl mx-auto h-full flex flex-col">
      <div className="mb-6 flex items-start justify-between gap-6">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-3">
            <h2 className="text-sm font-bold text-muted tracking-widest uppercase">Task Details</h2>
            <StatusBadge status={task.status} />
          </div>
          <p className="text-xl text-text leading-relaxed font-medium bg-surface p-5 rounded-2xl border border-border shadow-sm">
            {task.instruction}
          </p>
        </div>
      </div>

      {!isRunning && task.result_summary && (
        <div className={`mb-6 p-5 rounded-2xl border flex gap-4 ${
          task.status === 'complete' 
            ? 'bg-success/10 border-success/20 text-success' 
            : 'bg-error/10 border-error/20 text-error'
        }`}>
          <div className="mt-0.5">
            {task.status === 'complete' ? <CheckCircle2 size={20} /> : <AlertCircle size={20} />}
          </div>
          <div>
            <h3 className="font-semibold mb-1">
              {task.status === 'complete' ? 'Task Completed' : 'Task Failed'}
            </h3>
            <p className="opacity-90 leading-relaxed text-sm">{task.result_summary}</p>
          </div>
        </div>
      )}

      <h3 className="text-sm font-bold text-muted tracking-widest uppercase mb-3">Action Log</h3>
      <ActionLog logs={logs} isRunning={isRunning} />
    </div>
  );
}
