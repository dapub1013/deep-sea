"""
Track List Widget
Displays a scrollable list of tracks in the current show.
Part of the Player Screen left column.
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QLabel, QHBoxLayout
)

from ui.design_tokens import colors, typography, spacing, border_radius


class TrackListItem(QWidget):
    """Custom widget for individual track list items."""

    def __init__(self, track_number: int, track_title: str, duration: str, parent=None):
        super().__init__(parent)
        self.track_number = track_number
        self.track_title = track_title
        self.duration = duration

        self.setup_ui()

    def setup_ui(self):
        """Set up the track item layout."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            spacing.spacing_4,
            spacing.spacing_3,
            spacing.spacing_4,
            spacing.spacing_3
        )
        layout.setSpacing(spacing.spacing_3)

        # Track number
        number_label = QLabel(f"{self.track_number}.")
        number_label.setObjectName("track_number")
        number_label.setFixedWidth(30)
        number_label.setStyleSheet(f"""
            QLabel#track_number {{
                color: rgba(240, 240, 240, 0.5);
                font-size: {typography.body_size}px;
            }}
        """)
        layout.addWidget(number_label)

        # Track title
        title_label = QLabel(self.track_title)
        title_label.setObjectName("track_title")
        title_label.setStyleSheet(f"""
            QLabel#track_title {{
                color: {colors.foreground};
                font-size: {typography.body_size}px;
            }}
        """)
        layout.addWidget(title_label, 1)

        # Duration
        duration_label = QLabel(self.duration)
        duration_label.setObjectName("track_duration")
        duration_label.setStyleSheet(f"""
            QLabel#track_duration {{
                color: rgba(240, 240, 240, 0.7);
                font-size: {typography.caption_size}px;
            }}
        """)
        layout.addWidget(duration_label)


class TrackListWidget(QWidget):
    """
    Display a scrollable list of tracks.

    Signals:
        track_selected: Emitted when a track is selected (track_index)
    """

    # Signals
    track_selected = pyqtSignal(int)  # Emit track index

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tracks = []
        self.setup_ui()

        # Load placeholder data for testing
        self.load_placeholder_data()

    def setup_ui(self):
        """Set up the track list layout."""
        self.setObjectName("track_list_widget")

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, spacing.spacing_4, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QLabel("Tracks")
        header.setObjectName("h3")
        header.setStyleSheet(f"""
            QLabel#h3 {{
                color: {colors.foreground};
                font-size: {typography.h3_size}px;
                font-weight: {typography.weight_medium};
                padding-left: {spacing.spacing_4}px;
                padding-bottom: {spacing.spacing_2}px;
            }}
        """)
        layout.addWidget(header)

        # Track list
        self.list_widget = QListWidget()
        self.list_widget.setObjectName("track_list")
        self.list_widget.setStyleSheet(f"""
            QListWidget#track_list {{
                background-color: transparent;
                border: none;
                outline: none;
            }}
            QListWidget#track_list::item {{
                background-color: {colors.card};
                border: 1px solid {colors.border};
                border-radius: {border_radius.radius_md}px;
                margin: {spacing.spacing_2}px {spacing.spacing_4}px;
                padding: 0px;
            }}
            QListWidget#track_list::item:hover {{
                background-color: rgba(139, 92, 246, 0.25);
                border-color: {colors.primary};
            }}
            QListWidget#track_list::item:selected {{
                background-color: rgba(139, 92, 246, 0.35);
                border-color: {colors.primary};
            }}
        """)

        # Connect selection signal
        self.list_widget.currentRowChanged.connect(self.on_track_selected)

        layout.addWidget(self.list_widget)

    def load_placeholder_data(self):
        """Load placeholder tracks for testing."""
        placeholder_tracks = [
            {"title": "Tweezer", "duration": "12:34"},
            {"title": "Split Open and Melt", "duration": "8:45"},
            {"title": "Harry Hood", "duration": "15:22"},
            {"title": "You Enjoy Myself", "duration": "21:03"},
            {"title": "Chalk Dust Torture", "duration": "7:18"},
            {"title": "Cavern", "duration": "4:32"},
            {"title": "Down with Disease", "duration": "18:56"},
            {"title": "Mike's Song", "duration": "9:41"},
        ]
        self.set_tracks(placeholder_tracks)

    def set_tracks(self, tracks: list):
        """
        Update the track list.

        Args:
            tracks: List of dictionaries with keys:
                - title: str
                - duration: str (MM:SS format)
        """
        self.tracks = tracks
        self.list_widget.clear()

        for i, track in enumerate(tracks, start=1):
            # Create track item widget
            track_widget = TrackListItem(
                track_number=i,
                track_title=track['title'],
                duration=track['duration']
            )

            # Create list item
            item = QListWidgetItem(self.list_widget)
            item.setSizeHint(track_widget.sizeHint())

            # Add to list
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, track_widget)

    def on_track_selected(self, row: int):
        """Handle track selection."""
        if row >= 0:
            self.track_selected.emit(row)

    def set_current_track(self, track_index: int):
        """
        Highlight the currently playing track.

        Args:
            track_index: Index of the track (0-based)
        """
        if 0 <= track_index < self.list_widget.count():
            self.list_widget.setCurrentRow(track_index)
