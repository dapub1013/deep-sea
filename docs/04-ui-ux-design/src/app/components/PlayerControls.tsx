import { Play, Pause, SkipBack, SkipForward, RotateCcw, RotateCw } from "lucide-react";

interface PlayerControlsProps {
  isPlaying: boolean;
  onPlayPause: () => void;
  onPrevious: () => void;
  onNext: () => void;
  onRewind?: () => void;
  onSkip?: () => void;
  size?: "compact" | "large";
}

export function PlayerControls({ 
  isPlaying, 
  onPlayPause, 
  onPrevious, 
  onNext,
  onRewind,
  onSkip,
  size = "large"
}: PlayerControlsProps) {
  const iconSize = size === "compact" ? 20 : 28;
  const buttonSize = size === "compact" ? "min-w-[44px] min-h-[44px]" : "min-w-[56px] min-h-[56px]";
  const playButtonSize = size === "compact" ? "min-w-[44px] min-h-[44px]" : "min-w-[64px] min-h-[64px]";
  
  return (
    <div className="flex items-center justify-center gap-4">
      {onRewind && (
        <button
          onClick={onRewind}
          className={`${buttonSize} flex items-center justify-center rounded-full transition-all duration-200 active:scale-95 hover:bg-accent`}
          aria-label="Rewind 30 seconds"
        >
          <RotateCcw size={iconSize} />
        </button>
      )}
      
      <button
        onClick={onPrevious}
        className={`${buttonSize} flex items-center justify-center rounded-full transition-all duration-200 active:scale-95 hover:bg-accent`}
        aria-label="Previous track"
      >
        <SkipBack size={iconSize} />
      </button>
      
      <button
        onClick={onPlayPause}
        className={`${playButtonSize} flex items-center justify-center rounded-full bg-primary text-primary-foreground transition-all duration-200 active:scale-95 hover:bg-[var(--primary-hover)] shadow-lg`}
        aria-label={isPlaying ? "Pause" : "Play"}
      >
        {isPlaying ? <Pause size={iconSize + 4} /> : <Play size={iconSize + 4} />}
      </button>
      
      <button
        onClick={onNext}
        className={`${buttonSize} flex items-center justify-center rounded-full transition-all duration-200 active:scale-95 hover:bg-accent`}
        aria-label="Next track"
      >
        <SkipForward size={iconSize} />
      </button>
      
      {onSkip && (
        <button
          onClick={onSkip}
          className={`${buttonSize} flex items-center justify-center rounded-full transition-all duration-200 active:scale-95 hover:bg-accent`}
          aria-label="Skip 30 seconds"
        >
          <RotateCw size={iconSize} />
        </button>
      )}
    </div>
  );
}