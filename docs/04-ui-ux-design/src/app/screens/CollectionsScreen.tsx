import { useState } from "react";
import { useNavigate } from "react-router";
import { Plus, Trash2, ChevronLeft } from "lucide-react";
import { ShowCard } from "@/app/components/ShowCard";
import { mockShows } from "@/app/data/mockData";
import { usePlayerStore } from "@/app/store/playerStore";
import { ScrollArea } from "@/app/components/ui/scroll-area";

interface Collection {
  id: string;
  name: string;
  showIds: string[];
}

export function CollectionsScreen() {
  const navigate = useNavigate();
  const setCurrentShow = usePlayerStore(state => state.setCurrentShow);
  const setIsPlaying = usePlayerStore(state => state.setIsPlaying);
  
  const [collections, setCollections] = useState<Collection[]>([
    {
      id: "favorites",
      name: "⭐ Favorites",
      showIds: ["1997-12-31", "2024-07-21"]
    },
    {
      id: "attended",
      name: "🎫 Shows I Attended",
      showIds: ["2023-04-15"]
    }
  ]);

  const handleShowSelect = (showId: string) => {
    const show = mockShows.find(s => s.id === showId);
    if (show) {
      setCurrentShow(show);
      setIsPlaying(true);
      navigate("/player");
    }
  };

  const handleNewCollection = () => {
    const name = prompt("Enter collection name:");
    if (name) {
      setCollections([...collections, {
        id: Date.now().toString(),
        name,
        showIds: []
      }]);
    }
  };

  const handleDeleteCollection = (collectionId: string) => {
    if (confirm("Delete this collection?")) {
      setCollections(collections.filter(c => c.id !== collectionId));
    }
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
          <h1 className="text-title flex-1">Collections</h1>
          <button
            onClick={handleNewCollection}
            className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full bg-primary text-primary-foreground hover:bg-[var(--primary-hover)] transition-all duration-200 active:scale-95"
          >
            <Plus size={24} />
          </button>
        </div>
      </div>

      <div className="p-6">
        <ScrollArea className="h-[calc(100vh-200px)]">
          <div className="space-y-8">
            {collections.map(collection => {
              const shows = mockShows.filter(show => collection.showIds.includes(show.id));
              
              return (
                <div key={collection.id}>
                  <div className="flex items-center justify-between mb-3">
                    <h2 className="text-body font-medium">{collection.name}</h2>
                    <button
                      onClick={() => handleDeleteCollection(collection.id)}
                      className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full hover:bg-destructive/10 text-destructive transition-all duration-200"
                    >
                      <Trash2 size={20} />
                    </button>
                  </div>
                  
                  {shows.length === 0 ? (
                    <div className="p-8 text-center text-caption text-muted-foreground bg-muted rounded-xl">
                      No shows in this collection yet
                    </div>
                  ) : (
                    <div className="space-y-2">
                      {shows.map(show => (
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
                  )}
                </div>
              );
            })}
          </div>
        </ScrollArea>
      </div>
    </div>
  );
}