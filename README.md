# VulnDB

VulnDB is a backend application built with FastAPI and MongoDB to aggregate and manage security vulnerabilities from various vendors. It scrapes data from vendor-specific sources, stores it in a MongoDB database, and provides a RESTful API for querying vulnerabilities.

Built by Team Divya Utsav (Team ID 5568) for Smart India Hackathon 2024

Frontend: https://github.com/Namandas/OEM_Scrappper

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [License](#license)
- [Disclaimer](#disclaimer)

## Features

- **Data Scraping**: Automatically scrapes vulnerabilities from vendors.
- **MongoDB Storage**: Stores vulnerability data in a MongoDB database.
- **RESTful API**: Provides endpoints to query vulnerabilities by vendor and limit.
- **Vendor List**: Fetches a list of available vendors for vulnerability data.

## Technologies Used

- Python 3.x
- FastAPI
- MongoDB (via Motor for asynchronous operations)
- aiohttp (for making asynchronous HTTP requests)
- BeautifulSoup (for HTML parsing)
- Pydantic (for data validation)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Imyr/vulndb.git
   cd vulndb
   ```

2. **Create a virtual environment (optional but recommended)**:

   ```bash
   python -m venv .env
   source .env/bin/activate   # On Windows use `.env\Scripts\activate.bat`
   ```

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables**:
   - Create a `config.env` file in the project root directory with the following content:

     ```plaintext
     MONGODB_URL=mongodb://your_mongo_uri
     ```

5. **Run the application**:

   ```bash
   python -m vulndb
   ```

   The application will start at `http://0.0.0.0:6969`.

## Usage

Once the application is running, you can access the API endpoints using tools like [Postman](https://www.postman.com/) or `curl`. 

### Example Queries

- **Get the list of available vendors**:

   ```bash
   curl -X GET http://localhost:6969/available_vendors
   ```

- **Query vulnerabilities**:

   ```bash
   curl -X POST http://localhost:6969/vulnerabilities/list -H "Content-Type: application/json" -d '{"vendor": "Cisco", "limit": 10}'
   ```

- **Update vulnerabilities**:

   ```bash
   curl -X GET http://localhost:6969/vulnerabilities/update
   ```

## API Endpoints

- `GET /` - Returns basic information about the API.
- `GET /available_vendors` - Lists available vendors for vulnerabilities.
- `POST /vulnerabilities/list` - Queries vulnerabilities based on the provided vendor and limit in the request body.
- `GET /vulnerabilities/update` - Scrapes new vulnerabilities and updates the database.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer

This repository is for research purposes only, the use of this code is your responsibility. I take no responsibility and/or liability for how you choose to use any of the code available here. By using any of the files available here, you understand that you are agreeing to use at your own risk. Once again, all files available in this repository are for educational and/or research purposes only.

