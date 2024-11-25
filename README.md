# Web-Skeletonizer
Web Skeletonizer is a web application that extracts the structural HTML "skeleton" of a given webpage, removing unnecessary elements like scripts, styles, and media files. It also supports user authentication, allowing users to save and manage their skeletonized outputs for later use.

Features
User Registration and Login:

Users can register with a username, email, and password.
Secure login functionality (with session handling).
Skeleton Extraction:

Input a URL to extract the HTML structure of the webpage.
Remove scripts, styles, images, videos, and other unnecessary elements.
Save the skeletonized content locally as a .txt file.
Saved Skeleton Management:

List all previously saved skeleton files.
Fetch and view saved skeletons by their filenames.
Backend Functionality:

RESTful API endpoints for user authentication, skeletonization, and saved skeleton management.
Database:

User data (username, email, password) is stored in a MySQL database.

Project Directory Structure
bash
Copy code
Web Skeletonizer/
├── app.py                     # Flask Backend
├── saved_skeletons/           # Directory for storing skeleton files
├── frontend/                  # Optional React-based frontend
├── README.md                  # Project documentation


#Screenshots

HomePage
![Screenshot 2024-11-22 075815](https://github.com/user-attachments/assets/261db10f-dbd6-4911-8942-581033f55760)

Login
![Screenshot 2024-11-22 075916](https://github.com/user-attachments/assets/eee5aff7-c47d-4c78-a962-4c9fad512268)

Register
![Screenshot 2024-11-22 075848](https://github.com/user-attachments/assets/6285d4ef-1707-4c98-a026-63e8658582b9)

Dashboard
![Screenshot 2024-11-22 080018](https://github.com/user-attachments/assets/b13a3dbe-accd-46cd-ae09-595c8e3aa956)

Skeletonizer
![Screenshot 2024-11-22 080112](https://github.com/user-attachments/assets/b989ff00-fbf8-4bbd-9e80-81bf93ee2cd6)

Saved-Outputs
![Screenshot 2024-11-22 080201](https://github.com/user-attachments/assets/49073ea4-7679-47fc-909c-ff053556ccc8)






