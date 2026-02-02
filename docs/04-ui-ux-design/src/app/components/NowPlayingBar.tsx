import { useState } from "react";
import { useNavigate, useLocation } from "react-router";
import { ChevronDown, ChevronUp, X } from "lucide-react";
import { Equalizer } from "@/app/components/Equalizer";
import { PlayerControls } from "@/app/components/PlayerControls";
import { usePlayerStore } from "@/app/store/playerStore";
import { motion, AnimatePresence } from "motion/react";

export function NowPlayingBar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [isHidden, setIsHidden] = useState(false);
  const {
    currentShow,
    currentTrack,
    isPlaying,
    setIsPlaying,
    setCurrentShow,
    nextTrack,
    previousTrack,
  } = usePlayerStore();

  // Don't show on player screen
  const isOnPlayerScreen = location.pathname === "/player";
  
  if (!currentShow || !currentTrack || isOnPlayerScreen) return null;

  const handleClose = (e: React.MouseEvent) => {
    e.stopPropagation();
    setCurrentShow(null);
    setIsPlaying(false);
  };

  return (
    <AnimatePresence>
      {!isHidden && (
        <motion.div
          initial={{ y: 100 }}
          animate={{ y: 0 }}
          exit={{ y: 100 }}
          className="fixed bottom-0 left-0 right-0 bg-[#2d1b4e] border-t border-border z-30"
          style={{ boxShadow: "0 -2px 12px rgba(0, 0, 0, 0.3)" }}
        >
          <div className="max-w-screen-lg mx-auto">
            {/* Main bar - tap to expand */}
            <div
              onClick={() => navigate("/player")}
              className="w-full p-4 flex items-center gap-4 hover:bg-accent/30 transition-all duration-200 active:bg-accent/50 cursor-pointer"
            >
              {/* Close button */}
              <button
                onClick={handleClose}
                className="flex-shrink-0 min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full hover:bg-destructive/20 text-foreground hover:text-destructive transition-all duration-200"
              >
                <X size={24} />
              </button>

              {/* Show info */}
              <div className="flex-1 min-w-0 text-left">
                <div className="text-body font-medium truncate">
                  {currentTrack.title}
                </div>
                <div className="text-caption text-muted-foreground truncate">
                  {currentShow.date} • {currentShow.venue}
                </div>
              </div>

              {/* Centered equalizer */}
              <div className="flex-shrink-0">
                <Equalizer size="compact" isPlaying={isPlaying} />
              </div>

              {/* Compact controls */}
              <div className="flex-shrink-0" onClick={(e) => e.stopPropagation()}>
                <PlayerControls
                  isPlaying={isPlaying}
                  onPlayPause={() => setIsPlaying(!isPlaying)}
                  onPrevious={previousTrack}
                  onNext={nextTrack}
                  size="compact"
                />
              </div>
            </div>

            {/* Hide/show toggle */}
            <button
              onClick={() => setIsHidden(true)}
              className="w-full py-2 flex items-center justify-center hover:bg-accent/30 transition-all duration-200"
            >
              <ChevronDown size={20} className="text-muted-foreground" />
            </button>
          </div>
        </motion.div>
      )}

      {/* Show button when hidden */}
      {isHidden && currentShow && (
        <motion.button
          initial={{ y: 100 }}
          animate={{ y: 0 }}
          onClick={() => setIsHidden(false)}
          className="fixed bottom-4 right-4 w-12 h-12 flex items-center justify-center rounded-full bg-primary text-primary-foreground shadow-xl z-30 hover:scale-110 transition-all duration-200"
        >
          <ChevronUp size={24} />
        </motion.button>
      )}
    </AnimatePresence>
  );
}