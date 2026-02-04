"""
Phish.in API Client

Simple wrapper around requests for phish.in API calls.
"""

import logging
import requests
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class PhishInAPI:
    """
    Client for phish.in API.

    Provides methods for fetching shows, tours, and metadata from
    the phish.in API.
    """

    BASE_URL = "https://phish.in/api/v2"

    @staticmethod
    def get_shows(year: Optional[int] = None, audio_status: str = "complete") -> List[Dict]:
        """
        Get shows, optionally filtered by year and audio status.

        Args:
            year: Filter by year (optional)
            audio_status: Filter by audio status (default: "complete")

        Returns:
            List of show dictionaries
        """
        url = f"{PhishInAPI.BASE_URL}/shows"
        params = {"audio_status": audio_status}
        if year:
            params["year"] = year

        logger.debug(f"Fetching shows with params: {params}")

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            shows = data.get('shows', [])  # List endpoint returns 'shows' not 'data'
            logger.info(f"Fetched {len(shows)} shows")
            return shows
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch shows: {e}")
            raise

    @staticmethod
    def get_show(show_date: str) -> Dict:
        """
        Get a specific show by date.

        Args:
            show_date: Show date in YYYY-MM-DD format

        Returns:
            Show dictionary with metadata and tracks
        """
        url = f"{PhishInAPI.BASE_URL}/shows/{show_date}"

        logger.debug(f"Fetching show: {show_date}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            show = response.json()  # Response IS the show data (not wrapped)
            logger.info(f"Fetched show: {show_date}")
            return show
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch show {show_date}: {e}")
            raise

    @staticmethod
    def get_tours() -> List[Dict]:
        """
        Get all tours.

        Returns:
            List of tour dictionaries
        """
        url = f"{PhishInAPI.BASE_URL}/tours"

        logger.debug("Fetching tours")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            tours = data.get('tours', [])  # List endpoint returns 'tours' not 'data'
            logger.info(f"Fetched {len(tours)} tours")
            return tours
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch tours: {e}")
            raise

    @staticmethod
    def get_tour(tour_slug: str) -> Dict:
        """
        Get a specific tour by slug.

        Args:
            tour_slug: Tour slug identifier

        Returns:
            Tour dictionary with shows
        """
        url = f"{PhishInAPI.BASE_URL}/tours/{tour_slug}"

        logger.debug(f"Fetching tour: {tour_slug}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            tour = response.json()  # Response IS the tour data (not wrapped)
            logger.info(f"Fetched tour: {tour_slug}")
            return tour
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch tour {tour_slug}: {e}")
            raise

    @staticmethod
    def search_songs(query: str) -> List[Dict]:
        """
        Search for songs by name.

        Args:
            query: Song name search query

        Returns:
            List of song dictionaries
        """
        url = f"{PhishInAPI.BASE_URL}/songs"
        params = {"name": query}

        logger.debug(f"Searching songs: {query}")

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            songs = data.get('songs', [])  # List endpoint returns 'songs' not 'data'
            logger.info(f"Found {len(songs)} songs matching '{query}'")
            return songs
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to search songs: {e}")
            raise
