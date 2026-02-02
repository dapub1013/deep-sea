import { ChevronRight } from "lucide-react";

interface TourCardProps {
  tourName: string;
  showCount: number;
  dateRange: string;
  onClick: () => void;
}

export function TourCard({ tourName, showCount, dateRange, onClick }: TourCardProps) {
  return (
    <button
      onClick={onClick}
      className="w-full p-4 bg-card rounded-xl border border-border backdrop-blur-lg hover:bg-accent/50 active:scale-[0.98] transition-all duration-200 flex items-center justify-between gap-3"
      style={{ boxShadow: "var(--shadow-md)" }}
    >
      <div className="text-left flex-1">
        <div className="text-body font-medium text-foreground mb-1">{tourName}</div>
        <div className="text-caption text-muted-foreground">
          {showCount} {showCount === 1 ? 'show' : 'shows'} • {dateRange}
        </div>
      </div>
      <ChevronRight size={24} className="text-muted-foreground flex-shrink-0" />
    </button>
  );
}
