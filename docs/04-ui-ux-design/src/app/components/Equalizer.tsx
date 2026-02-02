import { motion } from "motion/react";
import { useEffect, useState } from "react";

interface EqualizerProps {
  size?: "compact" | "large";
  isPlaying?: boolean;
}

export function Equalizer({ size = "large", isPlaying = true }: EqualizerProps) {
  const barCount = 5;
  const [heights, setHeights] = useState<number[]>(Array(barCount).fill(0.3));

  // Dimensions based on size
  const dimensions = size === "compact" 
    ? { container: 40, barWidth: 5, gap: 3, maxHeight: 32 }
    : { container: 120, barWidth: 16, gap: 8, maxHeight: 96 };

  useEffect(() => {
    if (!isPlaying) {
      setHeights(Array(barCount).fill(0.3));
      return;
    }

    // Animate bars with different frequencies
    const intervals = heights.map((_, index) => {
      const baseSpeed = 200 + index * 100;
      return setInterval(() => {
        setHeights(prev => {
          const newHeights = [...prev];
          // Random height between 0.3 and 1.0
          newHeights[index] = 0.3 + Math.random() * 0.7;
          return newHeights;
        });
      }, baseSpeed);
    });

    return () => {
      intervals.forEach(interval => clearInterval(interval));
    };
  }, [isPlaying]);

  return (
    <div 
      className="flex items-end justify-center"
      style={{ 
        width: dimensions.container, 
        height: dimensions.container,
        gap: dimensions.gap
      }}
    >
      {heights.map((height, index) => {
        // Calculate gradient position (darker at bottom, lighter at top)
        const gradientPosition = index / (barCount - 1);
        const darkColor = "var(--equalizer-dark)";
        const midColor = "var(--equalizer-mid)";
        const lightColor = "var(--equalizer-light)";
        
        return (
          <motion.div
            key={index}
            className="rounded-md"
            style={{
              width: dimensions.barWidth,
              background: `linear-gradient(to top, ${darkColor}, ${midColor}, ${lightColor})`,
              originY: 1
            }}
            animate={{
              height: height * dimensions.maxHeight,
            }}
            transition={{
              duration: 0.15,
              ease: "easeOut"
            }}
          />
        );
      })}
    </div>
  );
}
