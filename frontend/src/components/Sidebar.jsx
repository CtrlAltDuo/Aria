import { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, PlusCircle, Settings, Sparkles, Server } from 'lucide-react';
import axios from 'axios';

export default function Sidebar() {
  const [backendStatus, setBackendStatus] = useState(false);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        await axios.get('http://localhost:8000/tasks', { timeout: 2000 });
        setBackendStatus(true);
      } catch (error) {
        setBackendStatus(false);
      }
    };
    checkStatus();
    const interval = setInterval(checkStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const navItems = [
    { to: '/dashboard', icon: <LayoutDashboard size={20} />, label: 'Dashboard' },
    { to: '/new-task', icon: <PlusCircle size={20} />, label: 'New Task' },
    { to: '/settings', icon: <Settings size={20} />, label: 'Settings' },
  ];

  return (
    <div className="w-64 h-full bg-surface border-r border-border flex flex-col pt-8 pb-4">
      <div className="px-6 flex items-center gap-2 mb-10 text-text">
        <Sparkles className="text-accent" size={24} />
        <h1 className="text-2xl font-bold tracking-tight">Aria</h1>
      </div>
      
      <nav className="flex-1 px-4 flex flex-col gap-2">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                isActive 
                  ? 'bg-accent/10 text-accent font-medium' 
                  : 'text-muted hover:bg-white/5 hover:text-text'
              }`
            }
          >
            {item.icon}
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="px-8 mt-auto flex items-center gap-3 text-sm font-medium text-muted">
        <Server size={16} />
        <span>Backend Status</span>
        <div 
          className={`w-2.5 h-2.5 rounded-full ml-auto shadow-sm ${
            backendStatus ? 'bg-success shadow-success/20' : 'bg-error shadow-error/20'
          }`}
          title={backendStatus ? 'Online' : 'Offline'}
        />
      </div>
    </div>
  );
}
