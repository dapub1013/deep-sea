interface ShowCardProps {
  date: string;
  venue: string;
  tour?: string;
  rating?: number;
  tags?: string[];
  onClick?: () => void;
}

export function ShowCard({ date, venue, tour, rating, tags, onClick }: ShowCardProps) {
  return (
    <button
      onClick={onClick}
      className="w-full min-h-[88px] p-4 bg-card rounded-xl text-left transition-all duration-200 active:scale-[0.98] hover:shadow-lg border border-border backdrop-blur-lg"
      style={{ boxShadow: "var(--shadow-md)" }}
    >
      <div className="flex flex-col gap-1">
        <div className="text-body font-medium text-foreground">{date}</div>
        <div className="text-caption text-muted-foreground">{venue}</div>
        {tour && (
          <div className="text-caption text-muted-foreground italic">{tour}</div>
        )}
        {(rating || tags) && (
          <div className="flex gap-2 mt-2 flex-wrap">
            {rating && (
              <span className="px-2 py-0.5 text-xs rounded-full bg-accent text-accent-foreground">
                ⭐ {rating.toFixed(1)}
              </span>
            )}
            {tags?.map((tag, i) => (
              <span 
                key={i}
                className="px-2 py-0.5 text-xs rounded-full bg-secondary text-secondary-foreground"
              >
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </button>
  );
}