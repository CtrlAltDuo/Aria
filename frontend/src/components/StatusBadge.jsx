export default function StatusBadge({ status }) {
  const configs = {
    pending: { color: 'bg-muted/20 text-muted', label: 'Pending' },
    running: { color: 'bg-accent/20 text-accent border border-accent/30', label: 'Running', animate: true },
    complete: { color: 'bg-success/20 text-success border border-success/30', label: 'Complete' },
    failed: { color: 'bg-error/20 text-error border border-error/30', label: 'Failed' },
    cancelled: { color: 'bg-muted/10 text-muted/50 line-through', label: 'Cancelled' }
  };

  const config = configs[status] || configs.pending;

  return (
    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium ${config.color}`}>
      {config.animate && (
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-accent"></span>
        </span>
      )}
      {config.label}
    </div>
  );
}
