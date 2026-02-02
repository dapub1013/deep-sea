import { createBrowserRouter } from "react-router";
import { Layout } from "@/app/Layout";
import { WelcomeScreen } from "@/app/screens/WelcomeScreen";
import { PlayerScreen } from "@/app/screens/PlayerScreen";
import { BrowseScreen } from "@/app/screens/BrowseScreen";
import { CollectionsScreen } from "@/app/screens/CollectionsScreen";
import { HistoryScreen } from "@/app/screens/HistoryScreen";
import { TourDetailScreen } from "@/app/screens/TourDetailScreen";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Layout,
    children: [
      { index: true, Component: WelcomeScreen },
      { path: "player", Component: PlayerScreen },
      { path: "browse", Component: BrowseScreen },
      { path: "collections", Component: CollectionsScreen },
      { path: "history", Component: HistoryScreen },
      { path: "tour/:tourSlug", Component: TourDetailScreen },
    ],
  },
]);