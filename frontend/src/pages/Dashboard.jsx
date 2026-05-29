import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import StatusBadge from '../components/StatusBadge';
import { Activity, CheckCircle2, ListTodo } from 'lucide-react';

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const res = await axios.get('http://localhost:8000/tasks');
        setTasks(res.data);
      } catch (error) {
        console.error('Failed to fetch tasks', error);
      }
    };
    fetchTasks();
    const interval = setInterval(fetchTasks, 2000);
    return () => clearInterval(interval);
  }, []);

  const stats = {
    total: tasks.length,
    completed: tasks.filter(t => t.status === 'complete').length,
    running: tasks.filter(t => t.status === 'running').length,
  };

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8">
      <header>
        <h2 className="text-3xl font-bold mb-2">Dashboard</h2>
        <p className="text-muted">Overview of Aria's activity</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard icon={<ListTodo className="text-blue-500" />} title="Total Tasks" value={stats.total} />
        <StatCard icon={<CheckCircle2 className="text-success" />} title="Completed" value={stats.completed} />
        <StatCard icon={<Activity className="text-accent" />} title="Running" value={stats.running} />
      </div>

      <div className="bg-surface border border-border rounded-2xl overflow-hidden shadow-sm">
        <div className="px-6 py-4 border-b border-border flex justify-between items-center bg-white/5">
          <h3 className="font-semibold">Recent Tasks</h3>
        </div>
        <div className="divide-y divide-border">
          {tasks.slice(0, 5).map(task => (
            <div 
              key={task.id} 
              onClick={() => navigate(`/task/${task.id}`)}
              className="px-6 py-4 flex items-center justify-between hover:bg-white/5 cursor-pointer transition-colors"
            >
              <div className="flex-1 mr-4 truncate">
                <p className="font-medium truncate text-text/90">{task.instruction}</p>
                <p className="text-xs text-muted mt-1">
                  {new Date(task.created_at).toLocaleString()}
                </p>
              </div>
              <StatusBadge status={task.status} />
            </div>
          ))}
          {tasks.length === 0 && (
            <div className="px-6 py-12 text-center text-muted text-sm">
              No tasks yet. Create one to get started!
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, title, value }) {
  return (
    <div className="bg-surface border border-border p-6 rounded-2xl flex items-center gap-4 shadow-sm hover:border-white/10 transition-colors">
      <div className="p-3 bg-white/5 rounded-xl border border-white/5">
        {icon}
      </div>
      <div>
        <p className="text-muted text-sm font-medium mb-1">{title}</p>
        <p className="text-3xl font-bold">{value}</p>
      </div>
    </div>
  );
}
