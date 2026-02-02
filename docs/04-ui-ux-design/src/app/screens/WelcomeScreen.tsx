import { PrimaryButton } from "@/app/components/PrimaryButton";
import { useNavigate } from "react-router";
import { getRandomShow, getTodayInHistory } from "@/app/data/mockData";
import { usePlayerStore } from "@/app/store/playerStore";

export function WelcomeScreen() {
  const navigate = useNavigate();
  const setCurrentShow = usePlayerStore(state => state.setCurrentShow);
  const setIsPlaying = usePlayerStore(state => state.setIsPlaying);
  
  const handleRandomShow = () => {
    const show = getRandomShow();
    setCurrentShow(show);
    setIsPlaying(true);
    navigate("/player");
  };
  
  const handleTodayInHistory = () => {
    const show = getTodayInHistory();
    if (show) {
      setCurrentShow(show);
      setIsPlaying(true);
      navigate("/player");
    }
  };
  
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8 pt-24 pb-24">
      <div className="w-full max-w-md space-y-8">
        {/* Logo placeholder */}
        <div className="flex flex-col items-center gap-4 mb-12">
          <div className="w-32 h-32 rounded-3xl bg-gradient-to-br from-[var(--purple-600)] to-[var(--purple-800)] flex items-center justify-center shadow-xl">
            <div className="text-white text-5xl">🐟</div>
          </div>
        </div>
        
        {/* Primary action buttons */}
        <div className="flex flex-col gap-4">
          <PrimaryButton 
            variant="primary"
            onClick={() => navigate("/browse")}
          >
            Find a show
          </PrimaryButton>
          
          <PrimaryButton 
            variant="secondary"
            onClick={handleRandomShow}
          >
            Random show
          </PrimaryButton>
          
          <PrimaryButton 
            variant="secondary"
            onClick={handleTodayInHistory}
          >
            Today in History
          </PrimaryButton>
        </div>
      </div>
    </div>
  );
}