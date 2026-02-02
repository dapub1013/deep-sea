import { Outlet, useLocation } from "react-router";
import { TopNav } from "@/app/components/TopNav";
import { NowPlayingBar } from "@/app/components/NowPlayingBar";

export function Layout() {
  const location = useLocation();
  
  // Only show navigation on welcome screen
  const showTopNav = location.pathname === "/";
  
  return (
    <div className="relative min-h-screen" style={{ 
      background: 'linear-gradient(180deg, #1a0b2e 0%, #2d1b4e 50%, #4c1d95 100%)',
      minHeight: '100vh'
    }}>
      {showTopNav && <TopNav />}
      <Outlet />
      <NowPlayingBar />
    </div>
  );
}