# Device Firmware Analytics

A web-based application for analyzing firmware data deployed on devices. It provides insights into firmware versions, device types, and historical firmware loading activities.

## Features

- Summaries of devices, firmware versions, and device types.
- Drill-down views for individual devices and firmware details.
- History of firmware loading activities.
- Interactive UI with hyperlinks for navigation.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- External MySQL Database

### Setup

1. Clone the Repository:

   ```bash
   git clone https://github.com/islepnev/afi-device-analytics.git
   cd afi-device-analytics
   ```

2. Prepare Environment Variables:
   - Copy the example `.env` file and update with your database credentials:

     ```bash
     cp .env.example .env
     ```

3. Build and Run the Application:

   ```bash
   docker-compose build
   docker-compose up
   ```

4. Access the Application:
   - Open your browser and navigate to `http://localhost:5000`.

### Usage

- Visit the home page to see total counts for devices, firmware versions, and device types.
- Click on any count to drill down into the details.
- View the history page for the latest firmware loading activities.

## Development

For local development, ensure you have Python 3.10 installed. Use the following commands:

1. Set up Virtual Environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install Dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the App Locally:

   ```bash
   python manage.py
   ```

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Author

- **Ilia Slepnev**
- GitHub: [islepnev](https://github.com/islepnev)
