import { Track } from "@/app/components/TrackList";

export interface Show {
  id: string;
  date: string;
  venue: string;
  location: string;
  tour: string;
  rating: number;
  tags: string[];
  tracks: Track[];
  sourceInfo: string;
}

export const mockShows: Show[] = [
  {
    id: "1997-12-31",
    date: "December 31, 1997",
    venue: "Madison Square Garden",
    location: "New York, NY",
    tour: "Fall Tour 1997",
    rating: 4.8,
    tags: ["NYE", "Epic"],
    sourceInfo: "AUD Master, Schoeps MK4",
    tracks: [
      { id: "t1", title: "AC/DC Bag", duration: 427, isJamchart: false },
      { id: "t2", title: "Golgi Apparatus", duration: 315, isJamchart: false },
      { id: "t3", title: "Runaway Jim", duration: 892, isJamchart: true, jamStartsAt: 420 },
      { id: "t4", title: "Train Song", duration: 198, isJamchart: false },
      { id: "t5", title: "Guyute", duration: 645, isJamchart: true, jamStartsAt: 320 },
      { id: "t6", title: "Lawn Boy", duration: 172, isJamchart: false },
      { id: "t7", title: "Tweezer", duration: 1243, isJamchart: true, jamStartsAt: 600 },
      { id: "t8", title: "Izabella", duration: 543, isJamchart: false },
    ]
  },
  {
    id: "2023-04-15",
    date: "April 15, 2023",
    venue: "The Forum",
    location: "Los Angeles, CA",
    tour: "Spring Tour 2023",
    rating: 4.5,
    tags: ["Great Setlist"],
    sourceInfo: "SBD Official Release",
    tracks: [
      { id: "t1", title: "Punch You in the Eye", duration: 512, isJamchart: false },
      { id: "t2", title: "Gumbo", duration: 423, isJamchart: false },
      { id: "t3", title: "Ghost", duration: 987, isJamchart: true, jamStartsAt: 480 },
      { id: "t4", title: "The Moma Dance", duration: 398, isJamchart: false },
      { id: "t5", title: "Farmhouse", duration: 287, isJamchart: false },
    ]
  },
  {
    id: "2022-08-05",
    date: "August 5, 2022",
    venue: "Dick's Sporting Goods Park",
    location: "Commerce City, CO",
    tour: "Summer Tour 2022",
    rating: 4.6,
    tags: ["Dick's"],
    sourceInfo: "Matrix Mix",
    tracks: [
      { id: "t1", title: "Wilson", duration: 342, isJamchart: false },
      { id: "t2", title: "Divided Sky", duration: 876, isJamchart: true, jamStartsAt: 410 },
      { id: "t3", title: "Reba", duration: 754, isJamchart: true, jamStartsAt: 380 },
      { id: "t4", title: "Stash", duration: 698, isJamchart: false },
    ]
  },
  {
    id: "2024-07-21",
    date: "July 21, 2024",
    venue: "Gorge Amphitheatre",
    location: "George, WA",
    tour: "Summer Tour 2024",
    rating: 4.7,
    tags: ["Gorge Magic"],
    sourceInfo: "Official SBD",
    tracks: [
      { id: "t1", title: "Chalk Dust Torture", duration: 612, isJamchart: true, jamStartsAt: 300 },
      { id: "t2", title: "Carini", duration: 834, isJamchart: true, jamStartsAt: 420 },
      { id: "t3", title: "Prince Caspian", duration: 523, isJamchart: false },
      { id: "t4", title: "Harry Hood", duration: 945, isJamchart: true, jamStartsAt: 520 },
    ]
  },
  {
    id: "2019-12-30",
    date: "December 30, 2019",
    venue: "Madison Square Garden",
    location: "New York, NY",
    tour: "NYE Run 2019",
    rating: 4.4,
    tags: ["NYE Run", "MSG"],
    sourceInfo: "AUD FLAC",
    tracks: [
      { id: "t1", title: "Party Time", duration: 234, isJamchart: false },
      { id: "t2", title: "Sample in a Jar", duration: 312, isJamchart: false },
      { id: "t3", title: "Tube", duration: 721, isJamchart: true, jamStartsAt: 350 },
      { id: "t4", title: "Everything's Right", duration: 892, isJamchart: true, jamStartsAt: 430 },
    ]
  },
  {
    id: "2021-10-30",
    date: "October 30, 2021",
    venue: "MGM Grand Garden Arena",
    location: "Las Vegas, NV",
    tour: "Fall Tour 2021",
    rating: 4.9,
    tags: ["Halloween", "Epic Jam"],
    sourceInfo: "SBD Official Release",
    tracks: [
      { id: "t1", title: "You Enjoy Myself", duration: 1456, isJamchart: true, jamStartsAt: 720 },
      { id: "t2", title: "The Lizards", duration: 687, isJamchart: false },
      { id: "t3", title: "Also Sprach Zarathustra > Reba > Also Sprach Zarathustra", duration: 2134, isJamchart: true, jamStartsAt: 900 },
      { id: "t4", title: "Fluffhead", duration: 892, isJamchart: true, jamStartsAt: 450 },
      { id: "t5", title: "Crosseyed and Painless", duration: 734, isJamchart: false },
    ]
  }
];

// Helper function to get available dates
export const getAvailableDates = (): Date[] => {
  return mockShows.map(show => {
    const [month, day, year] = show.date.split(' ');
    const monthIndex = new Date(`${month} 1, 2000`).getMonth();
    return new Date(parseInt(year.replace(',', '')), monthIndex, parseInt(day.replace(',', '')));
  });
};

// Helper to get today in history
export const getTodayInHistory = (): Show | null => {
  const today = new Date();
  const todayMonth = today.getMonth();
  const todayDay = today.getDate();
  
  const historicalShow = mockShows.find(show => {
    const [month, day] = show.date.split(' ');
    const monthIndex = new Date(`${month} 1, 2000`).getMonth();
    const dayNum = parseInt(day.replace(',', ''));
    return monthIndex === todayMonth && dayNum === todayDay;
  });
  
  return historicalShow || mockShows[0]; // Fallback to first show if no match
};

// Get random show
export const getRandomShow = (): Show => {
  return mockShows[Math.floor(Math.random() * mockShows.length)];
};