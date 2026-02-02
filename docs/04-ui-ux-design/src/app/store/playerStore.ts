import { create } from 'zustand';
import { Show } from '@/app/data/mockData';
import { Track } from '@/app/components/TrackList';

interface PlayerState {
  currentShow: Show | null;
  currentTrack: Track | null;
  isPlaying: boolean;
  currentTime: number;
  volume: number;
  setCurrentShow: (show: Show | null) => void;
  setCurrentTrack: (track: Track | null) => void;
  setIsPlaying: (playing: boolean) => void;
  setCurrentTime: (time: number) => void;
  setVolume: (volume: number) => void;
  playTrack: (track: Track) => void;
  nextTrack: () => void;
  previousTrack: () => void;
}

export const usePlayerStore = create<PlayerState>((set, get) => ({
  currentShow: null,
  currentTrack: null,
  isPlaying: false,
  currentTime: 0,
  volume: 0.7,
  
  setCurrentShow: (show) => set({ 
    currentShow: show,
    currentTrack: show?.tracks[0] || null,
    currentTime: 0
  }),
  
  setCurrentTrack: (track) => set({ currentTrack: track, currentTime: 0 }),
  setIsPlaying: (playing) => set({ isPlaying: playing }),
  setCurrentTime: (time) => set({ currentTime: time }),
  setVolume: (volume) => set({ volume }),
  
  playTrack: (track) => set({ currentTrack: track, currentTime: 0, isPlaying: true }),
  
  nextTrack: () => {
    const { currentShow, currentTrack } = get();
    if (!currentShow || !currentTrack) return;
    
    const currentIndex = currentShow.tracks.findIndex(t => t.id === currentTrack.id);
    const nextIndex = (currentIndex + 1) % currentShow.tracks.length;
    set({ 
      currentTrack: currentShow.tracks[nextIndex],
      currentTime: 0,
      isPlaying: true
    });
  },
  
  previousTrack: () => {
    const { currentShow, currentTrack } = get();
    if (!currentShow || !currentTrack) return;
    
    const currentIndex = currentShow.tracks.findIndex(t => t.id === currentTrack.id);
    const previousIndex = currentIndex === 0 ? currentShow.tracks.length - 1 : currentIndex - 1;
    set({ 
      currentTrack: currentShow.tracks[previousIndex],
      currentTime: 0,
      isPlaying: true
    });
  }
}));
