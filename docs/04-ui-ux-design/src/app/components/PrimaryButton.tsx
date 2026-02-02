import { ButtonHTMLAttributes } from "react";

interface PrimaryButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: "primary" | "secondary";
}

export function PrimaryButton({ 
  children, 
  variant = "primary", 
  className = "",
  ...props 
}: PrimaryButtonProps) {
  const baseStyles = "min-h-[44px] px-6 py-3 rounded-xl transition-all duration-200 active:scale-95 shadow-md";
  
  const variantStyles = variant === "primary"
    ? "bg-primary text-primary-foreground hover:bg-[var(--primary-hover)] shadow-[var(--shadow-md)]"
    : "bg-secondary text-secondary-foreground hover:bg-accent shadow-[var(--shadow-sm)]";

  return (
    <button 
      className={`${baseStyles} ${variantStyles} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
