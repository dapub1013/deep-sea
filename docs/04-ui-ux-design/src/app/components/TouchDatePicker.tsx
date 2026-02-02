import { useState } from "react";
import { ChevronLeft, ChevronRight, Calendar } from "lucide-react";

interface TouchDatePickerProps {
  availableDates: Date[];
  onDateSelect: (date: Date) => void;
  selectedDate?: Date;
}

export function TouchDatePicker({ availableDates, onDateSelect, selectedDate }: TouchDatePickerProps) {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [showYearPicker, setShowYearPicker] = useState(false);
  const [showMonthPicker, setShowMonthPicker] = useState(false);
  
  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  
  const monthNamesShort = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
  ];
  
  // Get available years from available dates
  const availableYears = Array.from(
    new Set(availableDates.map(d => d.getFullYear()))
  ).sort((a, b) => b - a); // Sort descending (newest first)
  
  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();
    
    return { daysInMonth, startingDayOfWeek };
  };
  
  const isDateAvailable = (date: Date) => {
    return availableDates.some(availableDate => 
      availableDate.getFullYear() === date.getFullYear() &&
      availableDate.getMonth() === date.getMonth() &&
      availableDate.getDate() === date.getDate()
    );
  };
  
  const isDateSelected = (date: Date) => {
    if (!selectedDate) return false;
    return selectedDate.getFullYear() === date.getFullYear() &&
           selectedDate.getMonth() === date.getMonth() &&
           selectedDate.getDate() === date.getDate();
  };
  
  const { daysInMonth, startingDayOfWeek } = getDaysInMonth(currentMonth);
  const days = Array.from({ length: daysInMonth }, (_, i) => i + 1);
  const blanks = Array.from({ length: startingDayOfWeek }, (_, i) => i);
  
  const previousMonth = () => {
    setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1));
  };
  
  const nextMonth = () => {
    setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1));
  };
  
  const selectYear = (year: number) => {
    setCurrentMonth(new Date(year, currentMonth.getMonth()));
    setShowYearPicker(false);
  };
  
  const selectMonth = (monthIndex: number) => {
    setCurrentMonth(new Date(currentMonth.getFullYear(), monthIndex));
    setShowMonthPicker(false);
  };
  
  // Year picker view
  if (showYearPicker) {
    return (
      <div className="w-full max-w-md mx-auto bg-card rounded-xl p-4 backdrop-blur-lg border border-border" style={{ boxShadow: "var(--shadow-md)" }}>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-title">Select Year</h3>
          <button
            onClick={() => setShowYearPicker(false)}
            className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full hover:bg-accent transition-all duration-200"
          >
            <Calendar size={20} />
          </button>
        </div>
        <div className="grid grid-cols-3 gap-2 max-h-[400px] overflow-y-auto">
          {availableYears.map(year => (
            <button
              key={year}
              onClick={() => selectYear(year)}
              className={`min-h-[44px] px-4 rounded-lg transition-all duration-200 ${
                year === currentMonth.getFullYear()
                  ? "bg-primary text-primary-foreground shadow-md"
                  : "bg-accent text-accent-foreground hover:bg-primary/30 active:scale-95"
              }`}
            >
              {year}
            </button>
          ))}
        </div>
      </div>
    );
  }
  
  // Month picker view
  if (showMonthPicker) {
    return (
      <div className="w-full max-w-md mx-auto bg-card rounded-xl p-4 backdrop-blur-lg border border-border" style={{ boxShadow: "var(--shadow-md)" }}>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-title">Select Month</h3>
          <button
            onClick={() => setShowMonthPicker(false)}
            className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full hover:bg-accent transition-all duration-200"
          >
            <Calendar size={20} />
          </button>
        </div>
        <div className="grid grid-cols-3 gap-2">
          {monthNames.map((month, index) => (
            <button
              key={month}
              onClick={() => selectMonth(index)}
              className={`min-h-[44px] px-4 rounded-lg transition-all duration-200 ${
                index === currentMonth.getMonth()
                  ? "bg-primary text-primary-foreground shadow-md"
                  : "bg-accent text-accent-foreground hover:bg-primary/30 active:scale-95"
              }`}
            >
              {monthNamesShort[index]}
            </button>
          ))}
        </div>
      </div>
    );
  }
  
  return (
    <div className="w-full max-w-md mx-auto bg-card rounded-xl p-4 backdrop-blur-lg border border-border" style={{ boxShadow: "var(--shadow-md)" }}>
      {/* Month navigation */}
      <div className="flex items-center justify-between mb-4">
        <button
          onClick={previousMonth}
          className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full hover:bg-accent transition-all duration-200"
        >
          <ChevronLeft size={24} />
        </button>
        
        <div className="flex gap-2">
          <button
            onClick={() => setShowMonthPicker(true)}
            className="px-3 py-1 rounded-lg hover:bg-accent transition-all duration-200 text-body font-medium"
          >
            {monthNames[currentMonth.getMonth()]}
          </button>
          <button
            onClick={() => setShowYearPicker(true)}
            className="px-3 py-1 rounded-lg hover:bg-accent transition-all duration-200 text-body font-medium"
          >
            {currentMonth.getFullYear()}
          </button>
        </div>
        
        <button
          onClick={nextMonth}
          className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full hover:bg-accent transition-all duration-200"
        >
          <ChevronRight size={24} />
        </button>
      </div>
      
      {/* Day labels */}
      <div className="grid grid-cols-7 gap-2 mb-2">
        {["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"].map(day => (
          <div key={day} className="text-center text-caption text-muted-foreground h-[44px] flex items-center justify-center">
            {day}
          </div>
        ))}
      </div>
      
      {/* Calendar grid */}
      <div className="grid grid-cols-7 gap-2">
        {blanks.map(blank => (
          <div key={`blank-${blank}`} className="h-[44px]" />
        ))}
        
        {days.map(day => {
          const date = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), day);
          const available = isDateAvailable(date);
          const selected = isDateSelected(date);
          
          return (
            <button
              key={day}
              onClick={() => available && onDateSelect(date)}
              disabled={!available}
              className={`min-h-[44px] min-w-[44px] flex items-center justify-center rounded-lg transition-all duration-200 ${
                selected
                  ? "bg-primary text-primary-foreground shadow-md"
                  : available
                  ? "bg-accent text-accent-foreground hover:bg-primary/30 active:scale-95"
                  : "text-muted-foreground/30 cursor-not-allowed"
              }`}
            >
              {day}
            </button>
          );
        })}
      </div>
    </div>
  );
}