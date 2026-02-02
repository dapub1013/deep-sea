import { useEffect } from "react";
import { useNavigate } from "react-router";
import { Home, Heart } from "lucide-react";
import { Equalizer } from "@/app/components/Equalizer";
import { PlayerControls } from "@/app/components/PlayerControls";
import { ProgressBar } from "@/app/components/ProgressBar";
import { VolumeControl } from "@/app/components/VolumeControl";
import { TrackList } from "@/app/components/TrackList";
import { usePlayerStore } from "@/app/store/playerStore";
import { ScrollArea } from "@/app/components/ui/scroll-area";

export function PlayerScreen() {
  const navigate = useNavigate();
  const {
    currentShow,
    currentTrack,
    isPlaying,
    currentTime,
    volume,
    setIsPlaying,
    setCurrentTime,
    setVolume,
    playTrack,
    nextTrack,
    previousTrack,
  } = usePlayerStore();

  // Simulate time progression
  useEffect(() => {
    if (!isPlaying || !currentTrack) return;

    const interval = setInterval(() => {
      setCurrentTime(currentTime + 1);
      
      // Auto-advance to next track when current one ends
      if (currentTime >= currentTrack.duration) {
        nextTrack();
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [isPlaying, currentTime, currentTrack, nextTrack, setCurrentTime]);

  if (!currentShow || !currentTrack) {
    navigate("/");
    return null;
  }

  const handleJumpToHighlight = () => {
    if (currentTrack.jamStartsAt) {
      setCurrentTime(currentTrack.jamStartsAt);
    }
  };

  const handleRewind = () => {
    setCurrentTime(Math.max(0, currentTime - 30));
  };

  const handleSkip = () => {
    if (currentTrack) {
      setCurrentTime(Math.min(currentTrack.duration, currentTime + 30));
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#0f0620]">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border bg-card/80 sticky top-0 z-20">
        <button
          onClick={() => navigate("/")}
          className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full hover:bg-accent transition-all duration-200"
        >
          <Home size={28} />
        </button>
        
        <div className="flex gap-2">
          <button className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full hover:bg-accent transition-all duration-200">
            <Heart size={24} />
          </button>
        </div>
      </div>

      {/* Two-column layout */}
      <div className="flex-1 grid grid-cols-2 gap-6 p-6 pb-32">
        {/* Left Column - Show Metadata & Setlist */}
        <div className="flex flex-col gap-6">
          {/* Show metadata */}
          <div className="bg-card rounded-xl p-6 border border-border" style={{ boxShadow: "var(--shadow-md)" }}>
            <h1 className="text-body mb-3">{currentShow.date}</h1>
            <div className="space-y-2">
              <div className="text-title text-foreground">{currentShow.venue}</div>
              <div className="text-body text-muted-foreground">{currentShow.location}</div>
              <div className="text-caption text-muted-foreground italic">{currentShow.tour}</div>
              
              <div className="flex gap-2 flex-wrap mt-4">
                <span className="px-3 py-1 text-xs rounded-full bg-accent text-accent-foreground">
                  ⭐ {currentShow.rating.toFixed(1)}
                </span>
                {currentShow.tags.map((tag, i) => (
                  <span key={i} className="px-3 py-1 text-xs rounded-full bg-secondary text-secondary-foreground">
                    {tag}
                  </span>
                ))}
              </div>
              
              <div className="text-caption text-muted-foreground pt-3 border-t border-border mt-3">
                {currentShow.sourceInfo}
              </div>
            </div>
          </div>

          {/* Track list */}
          <div className="bg-card rounded-xl p-6 border border-border backdrop-blur-lg flex-1" style={{ boxShadow: "var(--shadow-md)" }}>
            <h3 className="text-body font-medium mb-4">Set List</h3>
            <ScrollArea className="h-[calc(100vh-500px)]">
              <TrackList
                tracks={currentShow.tracks}
                currentTrackId={currentTrack.id}
                onTrackSelect={playTrack}
              />
            </ScrollArea>
          </div>
        </div>

        {/* Right Column - Now Playing & Controls */}
        <div className="flex flex-col gap-6">
          {/* Now Playing Card */}
          <div className="bg-card rounded-xl p-8 border border-border backdrop-blur-lg text-center flex-1 flex flex-col justify-center" style={{ boxShadow: "var(--shadow-lg)" }}>
            {/* Equalizer */}
            <div className="flex justify-center mb-8">
              <Equalizer size="large" isPlaying={isPlaying} />
            </div>

            {/* Current track info */}
            <div className="mb-6">
              <h2 className="text-title mb-2 line-clamp-2">{currentTrack.title}</h2>
              {currentTrack.isJamchart && (
                <button
                  onClick={handleJumpToHighlight}
                  className="mt-2 px-4 py-2 text-sm rounded-lg bg-primary/20 text-primary hover:bg-primary/30 transition-all duration-200 active:scale-95"
                >
                  🔥 Jump to Highlight
                </button>
              )}
            </div>

            {/* Progress bar */}
            <div className="mb-6">
              <ProgressBar
                currentTime={currentTime}
                duration={currentTrack.duration}
                onSeek={setCurrentTime}
              />
            </div>

            {/* Player controls */}
            <div className="mb-6">
              <PlayerControls
                isPlaying={isPlaying}
                onPlayPause={() => setIsPlaying(!isPlaying)}
                onPrevious={previousTrack}
                onNext={nextTrack}
                onRewind={handleRewind}
                onSkip={handleSkip}
                size="large"
              />
            </div>

            {/* Volume control */}
            <div className="flex justify-center">
              <VolumeControl volume={volume} onVolumeChange={setVolume} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}