interface ProgressBarProps {
  currentTime: number;
  duration: number;
  onSeek?: (time: number) => void;
}

export function ProgressBar({ currentTime, duration, onSeek }: ProgressBarProps) {
  const progress = duration > 0 ? (currentTime / duration) * 100 : 0;
  
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!onSeek) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const percentage = x / rect.width;
    const newTime = percentage * duration;
    onSeek(newTime);
  };

  return (
    <div className="w-full space-y-2">
      <div 
        className="h-[8px] bg-muted rounded-full overflow-hidden cursor-pointer"
        onClick={handleClick}
      >
        <div 
          className="h-full bg-primary transition-all duration-200"
          style={{ width: `${progress}%` }}
        />
      </div>
      <div className="flex justify-between text-caption text-muted-foreground">
        <span>{formatTime(currentTime)}</span>
        <span>{formatTime(duration)}</span>
      </div>
    </div>
  );
}
