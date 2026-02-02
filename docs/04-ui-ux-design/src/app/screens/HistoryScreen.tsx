import { useState } from "react";
import { useNavigate } from "react-router";
import { ChevronLeft } from "lucide-react";
import { ShowCard } from "@/app/components/ShowCard";
import { mockShows } from "@/app/data/mockData";
import { usePlayerStore } from "@/app/store/playerStore";
import { ScrollArea } from "@/app/components/ui/scroll-area";

interface HistoryEntry {
  showId: string;
  playedAt: Date;
}

export function HistoryScreen() {
  const navigate = useNavigate();
  const setCurrentShow = usePlayerStore(state => state.setCurrentShow);
  const setIsPlaying = usePlayerStore(state => state.setIsPlaying);
  
  // Mock listening history
  const [history] = useState<HistoryEntry[]>([
    { showId: "2024-07-21", playedAt: new Date("2026-02-02T14:30:00") },
    { showId: "2022-08-05", playedAt: new Date("2026-02-01T19:45:00") },
    { showId: "1997-12-31", playedAt: new Date("2026-01-31T20:15:00") },
    { showId: "2023-04-15", playedAt: new Date("2026-01-30T16:20:00") },
  ]);

  const handleShowSelect = (showId: string) => {
    const show = mockShows.find(s => s.id === showId);
    if (show) {
      setCurrentShow(show);
      setIsPlaying(true);
      navigate("/player");
    }
  };

  const formatPlayedAt = (date: Date) => {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 60) return `${diffMins} minutes ago`;
    if (diffHours < 24) return `${diffHours} hours ago`;
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays} days ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="min-h-screen pb-32">
      {/* Header */}
      <div className="sticky top-0 z-20 backdrop-blur-lg border-b border-border bg-card/50">
        <div className="flex items-center p-4">
          <button
            onClick={() => navigate("/")}
            className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full hover:bg-accent transition-all duration-200 mr-2"
          >
            <ChevronLeft size={28} />
          </button>
          <h1 className="text-title">Listening History</h1>
        </div>
      </div>

      <div className="p-6">
        {history.length === 0 ? (
          <div className="p-12 text-center text-caption text-muted-foreground bg-muted rounded-xl">
            No listening history yet. Start exploring shows!
          </div>
        ) : (
          <ScrollArea className="h-[calc(100vh-200px)]">
            <div className="space-y-4">
              {history.map((entry, index) => {
                const show = mockShows.find(s => s.id === entry.showId);
                if (!show) return null;
                
                return (
                  <div key={index}>
                    <div className="text-caption text-muted-foreground mb-1">
                      {formatPlayedAt(entry.playedAt)}
                    </div>
                    <ShowCard
                      date={show.date}
                      venue={show.venue}
                      tour={show.tour}
                      rating={show.rating}
                      tags={show.tags}
                      onClick={() => handleShowSelect(show.id)}
                    />
                  </div>
                );
              })}
            </div>
          </ScrollArea>
        )}
      </div>
    </div>
  );
}