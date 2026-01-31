# Project Charter Discussion

## Purpose and Users
I will be the primary user of this application but I will most likely make the repo public on GitHub once it's complete. By "stream live concerts" I mean I want to develop a player that will play the concerts available on phish.in. This application is not attempting to solve any problems; this is a hobby project.

## Scope and Platform
I will ultimately run this software on a Raspberry Pi 4 with an IQAudio DAC. However, since I will be developing the application using a laptop running macOS, I would also like to use it on macOS. The more universal the application is the better. I am the sole developer.

## My Background
I have many years of experience in web development working with HTML, CSS and JavaScript. I have an eye for design. I am good with HTML and CSS. I do not write JS or use other languages but I am comfortable working with code. I have recently developed a similar application that streams Grateful Dead concerts via archive.org's API. While working on that project, I leveraged Claude and, eventually, Claude Code to write the software. I used Visual Code as my IDE. I am the sole developer. I have no time constraints. I learned a lot working on my Grateful Dead project, and I want to continue improving my skills with Claude Code. I also intend to use this project as a framework to update my Grateful Dead streaming software, i.e., lessons learned here will be used to create an updated version of that application.

## Phish.in API Documentation
Phish.in API documentation is here: [Phish.in API Docs](https://phish.in/api-docs).

Some notes from the page: Phish.in provides programmatic access to content for free via a RESTful JSON API. Version 2 is the latest stable version and is recommended. Additionally, an MCP (Model Context Protocol) server is available for AI assistant integration. Phish.in exposes data through a Model Context Protocol (MCP) server, enabling AI assistants and other MCP clients to interact with the platform using natural language. The server is read-only and does not require authentication.

### Endpoint
```
POST https://phish.in/mcp
```

### Available Tools
- **search** - Search across shows, songs, venues, tours, tags, and playlists
- **list_shows** - List shows with optional setlist details, filtered by year, tour, venue, or date
- **list_songs** - List songs with performance statistics
- **list_venues** - List venues with geographic filtering
- **list_tours** - List tours with date ranges and show counts
- **list_years** - List years/periods with show counts and era designations
- **get_song** - Get detailed song information including performances and lyrics
- **get_venue** - Get venue details with show history
- **get_tour** - Get tour details with associated shows
- **get_playlist** - Get public playlist details
- **stats** - Statistical analysis: gaps/bustouts, transitions, set positions, predictions, streaks, geographic patterns, co-occurrence, song frequency
