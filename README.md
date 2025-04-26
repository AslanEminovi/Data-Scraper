# Google Maps Scraper

A powerful data scraping application that allows you to extract business information from Google Maps, including contact details, ratings, and more. The application features a modern UI with both desktop and mobile interfaces.

## Features

- **Google Maps Data Extraction**
  - Search businesses by sector and city
  - Extract business names, addresses, ratings, phone numbers, and websites
  - Export data to Excel with automatic formatting

- **WhatsApp Integration**
  - Check if phone numbers are on WhatsApp
  - Direct WhatsApp chat initiation
  - Bulk WhatsApp number verification

- **AI Assistant**
  - Built-in AI chat interface
  - Ask questions about the data
  - Get insights and analysis

- **Modern UI**
  - Dark/Light theme support
  - Responsive design
  - User-friendly interface
  - Mobile app support (React Native)

## Tech Stack

### Desktop Application
- Python 3.x
- Tkinter with ttkbootstrap for modern UI
- Selenium for WhatsApp integration
- Google Maps API
- RapidAPI for AI features

### Mobile Application
- React Native
- React Navigation
- React Native Paper
- AsyncStorage for data persistence

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/AslanEminovi/Data-Scraper.git
   cd Data-Scraper
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js Dependencies**
   ```bash
   npm install
   ```

4. **Environment Variables**
   Create a `.env` file in the root directory with:
   ```
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   RAPIDAPI_KEY=your_rapidapi_key
   RAPIDAPI_HOST=your_rapidapi_host
   ```

5. **ChromeDriver Setup**
   - Download ChromeDriver compatible with your Chrome version
   - Place it in `C:\Program Files\chromedriver-win64\chromedriver.exe`
   - Or update the path in `main.py`

## Usage

1. **Desktop Application**
   ```bash
   python main.py
   ```
   - Enter sector and city
   - Click "Veri Çek" to fetch data
   - Use "Excel'e Aktar" to export
   - Check WhatsApp numbers with "WhatsApp Kontrol"
   - Open AI assistant with "Yapay Zeka Aç"

2. **Mobile Application**
   ```bash
   npm start
   ```
   - Use the React Native app for on-the-go data access
   - Same features as desktop version
   - Optimized for mobile use

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Maps API
- RapidAPI
- ttkbootstrap
- React Native community