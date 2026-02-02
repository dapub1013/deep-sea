import { Heart, Clock } from "lucide-react";
import { useNavigate, useLocation } from "react-router";

export function TopNav() {
  const navigate = useNavigate();
  const location = useLocation();
  
  const navItems = [
    { icon: Heart, label: "Collections", path: "/collections" },
    { icon: Clock, label: "History", path: "/history" },
  ];
  
  return (
    <nav className="fixed top-0 left-0 right-0 bg-[#2d1b4e] border-b border-border z-40 backdrop-blur-lg"
         style={{ boxShadow: "0 2px 8px rgba(0, 0, 0, 0.3)" }}>
      <div className="flex justify-around items-center h-[72px] max-w-screen-lg mx-auto">
        {navItems.map(({ icon: Icon, label, path }) => {
          const isActive = location.pathname === path;
          return (
            <button
              key={path}
              onClick={() => navigate(path)}
              className={`flex flex-col items-center justify-center min-w-[72px] min-h-[56px] gap-1 transition-colors ${
                isActive ? "text-primary" : "text-muted-foreground"
              }`}
            >
              <Icon size={24} />
              <span className="text-xs">{label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}