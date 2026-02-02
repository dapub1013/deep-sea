import { useNavigate, useParams } from "react-router";
import { ChevronLeft } from "lucide-react";
import { ShowCard } from "@/app/components/ShowCard";
import { mockShows } from "@/app/data/mockData";
import { usePlayerStore } from "@/app/store/playerStore";

export function TourDetailScreen() {
  const navigate = useNavigate();
  const { tourSlug } = useParams();
  const setCurrentShow = usePlayerStore(state => state.setCurrentShow);
  const setIsPlaying = usePlayerStore(state => state.setIsPlaying);
  
  // Decode tour name from slug
  const tourName = tourSlug?.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) || '';
  
  // Get shows for this tour
  const tourShows = mockShows.filter(show => 
    show.tour.toLowerCase() === tourName.toLowerCase()
  );

  const handleShowSelect = (showId: string) => {
    const show = mockShows.find(s => s.id === showId);
    if (show) {
      setCurrentShow(show);
      setIsPlaying(true);
      navigate("/player");
    }
  };

  return (
    <div className="min-h-screen pb-32">
      {/* Header */}
      <div className="sticky top-0 z-20 backdrop-blur-lg border-b border-border bg-card/50">
        <div className="flex items-center p-4">
          <button
            onClick={() => navigate(-1)}
            className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full hover:bg-accent transition-all duration-200 mr-2"
          >
            <ChevronLeft size={28} />
          </button>
          <h1 className="text-title">{tourName}</h1>
        </div>
      </div>

      {/* Shows grid - 3 columns */}
      <div className="p-6">
        <p className="text-caption text-muted-foreground mb-4">
          {tourShows.length} {tourShows.length === 1 ? 'show' : 'shows'}
        </p>
        <div className="grid grid-cols-3 gap-3">
          {tourShows.map(show => (
            <ShowCard
              key={show.id}
              date={show.date}
              venue={show.venue}
              rating={show.rating}
              tags={show.tags}
              onClick={() => handleShowSelect(show.id)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
