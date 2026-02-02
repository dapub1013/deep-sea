import { Volume2, VolumeX } from "lucide-react";
import { Slider } from "@/app/components/ui/slider";

interface VolumeControlProps {
  volume: number;
  onVolumeChange: (volume: number) => void;
}

export function VolumeControl({ volume, onVolumeChange }: VolumeControlProps) {
  const isMuted = volume === 0;
  
  return (
    <div className="flex items-center gap-3 w-full max-w-[200px]">
      <button
        onClick={() => onVolumeChange(isMuted ? 0.5 : 0)}
        className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full hover:bg-accent transition-all duration-200"
        aria-label={isMuted ? "Unmute" : "Mute"}
      >
        {isMuted ? <VolumeX size={20} /> : <Volume2 size={20} />}
      </button>
      <Slider
        value={[volume * 100]}
        onValueChange={(values) => onVolumeChange(values[0] / 100)}
        max={100}
        step={1}
        className="flex-1"
      />
    </div>
  );
}
