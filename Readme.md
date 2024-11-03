# Busniess Managment API

## Overview

The Receipt Processing API is a powerful tool developed using Flask. This application allows users to upload and process receipts to extract essential data. It is designed for use in financial management, expense tracking, and any scenario where automated receipt processing is beneficial.

## Features

1. **User Authentication:** The application supports user authentication to ensure that only authorized users can upload and process receipts.

2. **Receipt Upload:** Users can upload receipt images or PDFs through a simple interface.

3. **Data Extraction:** The application extracts key information from the receipts, such as vendor name, date, total amount, and line items.

4. **Data Storage:** Extracted data is stored in a structured format in a database for easy retrieval and analysis.

5. **API Endpoints:** Provides RESTful API endpoints for uploading receipts, retrieving processed data, and managing user accounts.

6. **Error Handling:** Comprehensive error handling to manage invalid uploads, unsupported file formats, and other potential issues.

## Installation

1. Clone the repository from GitHub: [GitHub Project](https://github.com/The-Hustler-Hattab/ReceiptManagementFlask).

2. Navigate to the project directory.

3. Create a virtual environment:
    ```bash
    $ python3 -m venv venv
    ```

4. Activate the virtual environment:
    - On Windows:
        ```bash
        $ venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        $ source venv/bin/activate
        ```

5. Install the required dependencies:
    ```bash
    $ pip install -r requirements.txt
    ```

6. Run the application:
    ```bash
    $ flask run
    ```


## Technologies Used

- **Flask:** Python micro web framework used for building the web application.
- **AZURE Form Recognizer:** Optical character recognition engine for extracting text from PDF.
- **MySQL:** Relational database used for storing extracted receipt data.
- **JWT:** JSON Web Tokens for secure user authentication.


## Contribution

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to reach out if you have any questions or need further assistance. Happy coding!
