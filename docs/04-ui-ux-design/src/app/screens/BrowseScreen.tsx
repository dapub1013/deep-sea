import { useState } from "react";
import { useNavigate } from "react-router";
import { TouchDatePicker } from "@/app/components/TouchDatePicker";
import { ShowCard } from "@/app/components/ShowCard";
import { TourCard } from "@/app/components/TourCard";
import { mockShows, getAvailableDates } from "@/app/data/mockData";
import { usePlayerStore } from "@/app/store/playerStore";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/app/components/ui/tabs";
import { ScrollArea } from "@/app/components/ui/scroll-area";
import { ChevronLeft } from "lucide-react";

export function BrowseScreen() {
  const navigate = useNavigate();
  const setCurrentShow = usePlayerStore(state => state.setCurrentShow);
  const setIsPlaying = usePlayerStore(state => state.setIsPlaying);
  const [selectedDate, setSelectedDate] = useState<Date | undefined>();
  const availableDates = getAvailableDates();

  const handleDateSelect = (date: Date) => {
    setSelectedDate(date);
    // Find the show for this date
    const show = mockShows.find(s => {
      const showDate = new Date(s.date);
      return showDate.getDate() === date.getDate() &&
             showDate.getMonth() === date.getMonth() &&
             showDate.getFullYear() === date.getFullYear();
    });
    
    if (show) {
      setCurrentShow(show);
      setIsPlaying(true);
      navigate("/player");
    }
  };

  const handleShowSelect = (showId: string) => {
    const show = mockShows.find(s => s.id === showId);
    if (show) {
      setCurrentShow(show);
      setIsPlaying(true);
      navigate("/player");
    }
  };

  // Group shows by tour
  const showsByTour = mockShows.reduce((acc, show) => {
    if (!acc[show.tour]) {
      acc[show.tour] = [];
    }
    acc[show.tour].push(show);
    return acc;
  }, {} as Record<string, typeof mockShows>);

  // Create tour metadata
  const tours = Object.entries(showsByTour).map(([tourName, shows]) => {
    const dates = shows.map(s => new Date(s.date));
    const minDate = new Date(Math.min(...dates.map(d => d.getTime())));
    const maxDate = new Date(Math.max(...dates.map(d => d.getTime())));
    
    return {
      name: tourName,
      slug: tourName.toLowerCase().replace(/\s+/g, '-'),
      showCount: shows.length,
      dateRange: minDate.getFullYear() === maxDate.getFullYear() 
        ? `${minDate.getFullYear()}`
        : `${minDate.getFullYear()}-${maxDate.getFullYear()}`
    };
  });

  // Get recent shows (last 3)
  const recentShows = [...mockShows].slice(0, 3);

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
          <h1 className="text-title">Browse Shows</h1>
        </div>
      </div>

      <div className="p-6">
        <Tabs defaultValue="calendar" className="w-full">
          <TabsList className="grid w-full grid-cols-3 mb-6">
            <TabsTrigger value="calendar">Calendar</TabsTrigger>
            <TabsTrigger value="tours">Tours</TabsTrigger>
            <TabsTrigger value="recent">Recent</TabsTrigger>
          </TabsList>
          
          <TabsContent value="calendar" className="space-y-4">
            <TouchDatePicker
              availableDates={availableDates}
              onDateSelect={handleDateSelect}
              selectedDate={selectedDate}
            />
            <p className="text-caption text-center text-muted-foreground">
              Tap month or year to quickly jump to any date
            </p>
          </TabsContent>
          
          <TabsContent value="tours">
            <ScrollArea className="h-[500px]">
              <div className="space-y-3">
                {tours.map(tour => (
                  <TourCard
                    key={tour.slug}
                    tourName={tour.name}
                    showCount={tour.showCount}
                    dateRange={tour.dateRange}
                    onClick={() => navigate(`/tour/${tour.slug}`)}
                  />
                ))}
              </div>
            </ScrollArea>
          </TabsContent>
          
          <TabsContent value="recent">
            <div className="space-y-2">
              <p className="text-caption text-muted-foreground mb-4">
                Recently performed shows
              </p>
              {recentShows.map(show => (
                <ShowCard
                  key={show.id}
                  date={show.date}
                  venue={show.venue}
                  tour={show.tour}
                  rating={show.rating}
                  tags={show.tags}
                  onClick={() => handleShowSelect(show.id)}
                />
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}