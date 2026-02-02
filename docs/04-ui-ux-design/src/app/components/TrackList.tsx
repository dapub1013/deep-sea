import { Play } from "lucide-react";

export interface Track {
  id: string;
  title: string;
  duration: number;
  isJamchart?: boolean;
  jamStartsAt?: number;
}

interface TrackListProps {
  tracks: Track[];
  currentTrackId?: string;
  onTrackSelect: (track: Track) => void;
}

export function TrackList({ tracks, currentTrackId, onTrackSelect }: TrackListProps) {
  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };
  
  return (
    <div className="space-y-1">
      {tracks.map((track) => {
        const isActive = track.id === currentTrackId;
        return (
          <button
            key={track.id}
            onClick={() => onTrackSelect(track)}
            className={`w-full min-h-[56px] px-4 py-2 flex items-center gap-3 rounded-lg transition-all duration-200 ${
              isActive 
                ? "bg-accent text-accent-foreground" 
                : "hover:bg-muted/50 active:bg-muted"
            }`}
          >
            <div className="min-w-[32px] min-h-[32px] flex items-center justify-center">
              {isActive ? (
                <div className="w-4 h-4 flex items-center justify-center">
                  <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
                </div>
              ) : (
                <Play size={16} className="text-muted-foreground" />
              )}
            </div>
            
            <div className="flex-1 text-left min-w-0">
              <div className="text-body truncate">{track.title}</div>
              {track.isJamchart && (
                <div className="flex gap-2 mt-1">
                  <span className="text-xs px-2 py-0.5 rounded-full bg-primary/10 text-primary">
                    🔥 Jamchart
                  </span>
                </div>
              )}
            </div>
            
            <div className="text-caption text-muted-foreground">
              {formatDuration(track.duration)}
            </div>
          </button>
        );
      })}
    </div>
  );
}
