"""
Show Metadata Widget
Displays show information: venue, date, location, source details.
Part of the Player Screen left column.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PyQt5.QtGui import QPixmap

from ui.design_tokens import colors, typography, spacing, border_radius


class ShowMetadataWidget(QWidget):
    """
    Display show metadata with album art and information.

    Components:
    - Album art (square image)
    - Venue name
    - Show date
    - Location (city, state)
    - Source info (if available)
    - Favorite button (heart icon)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

        # Load placeholder data for testing
        self.load_placeholder_data()

    def setup_ui(self):
        """Set up the metadata display layout."""
        self.setObjectName("show_metadata_widget")

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            spacing.spacing_4,
            spacing.spacing_4,
            spacing.spacing_4,
            spacing.spacing_4
        )
        layout.setSpacing(spacing.spacing_4)

        # Top row: Album art + metadata
        top_row = QHBoxLayout()
        top_row.setSpacing(spacing.spacing_4)

        # Album art
        self.album_art = QLabel()
        self.album_art.setObjectName("album_art")
        self.album_art.setFixedSize(120, 120)
        self.album_art.setScaledContents(True)
        self.album_art.setStyleSheet(f"""
            QLabel#album_art {{
                background-color: {colors.card};
                border-radius: {border_radius.radius_lg}px;
                border: 1px solid {colors.border};
            }}
        """)
        top_row.addWidget(self.album_art)

        # Metadata column
        metadata_col = QVBoxLayout()
        metadata_col.setSpacing(spacing.spacing_2)

        # Venue name
        self.venue_label = QLabel("Venue Name")
        self.venue_label.setObjectName("h2")
        self.venue_label.setStyleSheet(f"""
            QLabel#h2 {{
                color: {colors.foreground};
                font-size: {typography.h2_size}px;
                font-weight: {typography.weight_medium};
            }}
        """)
        metadata_col.addWidget(self.venue_label)

        # Show date
        self.date_label = QLabel("YYYY-MM-DD")
        self.date_label.setObjectName("h3")
        self.date_label.setStyleSheet(f"""
            QLabel#h3 {{
                color: {colors.primary};
                font-size: {typography.h3_size}px;
                font-weight: {typography.weight_medium};
            }}
        """)
        metadata_col.addWidget(self.date_label)

        # Location
        self.location_label = QLabel("City, State")
        self.location_label.setObjectName("caption")
        self.location_label.setStyleSheet(f"""
            QLabel#caption {{
                color: rgba(240, 240, 240, 0.7);
                font-size: {typography.caption_size}px;
            }}
        """)
        metadata_col.addWidget(self.location_label)

        # Source info
        self.source_label = QLabel("Source: Matrix • SBD")
        self.source_label.setObjectName("caption")
        self.source_label.setStyleSheet(f"""
            QLabel#caption {{
                color: rgba(240, 240, 240, 0.5);
                font-size: {typography.caption_size}px;
            }}
        """)
        metadata_col.addWidget(self.source_label)

        metadata_col.addStretch()
        top_row.addLayout(metadata_col, 1)

        # Favorite button
        self.favorite_btn = QPushButton("♥")
        self.favorite_btn.setObjectName("favorite_btn")
        self.favorite_btn.setFixedSize(
            spacing.touch_target,
            spacing.touch_target
        )
        self.favorite_btn.setStyleSheet(f"""
            QPushButton#favorite_btn {{
                background-color: {colors.card};
                color: {colors.primary};
                border: 1px solid {colors.border};
                border-radius: {border_radius.radius_lg}px;
                font-size: 20px;
            }}
            QPushButton#favorite_btn:hover {{
                background-color: rgba(139, 92, 246, 0.25);
                color: {colors.primary_hover};
            }}
            QPushButton#favorite_btn:pressed {{
                background-color: rgba(139, 92, 246, 0.35);
            }}
        """)
        top_row.addWidget(self.favorite_btn, alignment=Qt.AlignTop)

        layout.addLayout(top_row)

        # Divider
        divider = QWidget()
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"background-color: {colors.border};")
        layout.addWidget(divider)

    def load_placeholder_data(self):
        """Load placeholder data for testing."""
        self.set_show_data({
            'venue': 'Madison Square Garden',
            'date': '1997-12-31',
            'location': 'New York, NY',
            'source': 'Matrix • SBD',
            'album_art_url': None  # Will show placeholder
        })

    def set_show_data(self, show_data: dict):
        """
        Update the widget with show data.

        Args:
            show_data: Dictionary with keys:
                - venue: str
                - date: str (YYYY-MM-DD)
                - location: str (City, State)
                - source: str (optional)
                - album_art_url: str (optional)
        """
        self.venue_label.setText(show_data.get('venue', 'Unknown Venue'))
        self.date_label.setText(show_data.get('date', 'Unknown Date'))
        self.location_label.setText(show_data.get('location', 'Unknown Location'))

        source = show_data.get('source')
        if source:
            self.source_label.setText(f"Source: {source}")
            self.source_label.show()
        else:
            self.source_label.hide()

        # Load album art if URL provided
        album_art_url = show_data.get('album_art_url')
        if album_art_url:
            # TODO: Load image from URL or cache
            pass
        else:
            # Show placeholder
            self.album_art.setText("♪")
            self.album_art.setAlignment(Qt.AlignCenter)
            self.album_art.setStyleSheet(f"""
                QLabel#album_art {{
                    background-color: {colors.card};
                    border-radius: {border_radius.radius_lg}px;
                    border: 1px solid {colors.border};
                    color: {colors.primary};
                    font-size: 48px;
                }}
            """)
