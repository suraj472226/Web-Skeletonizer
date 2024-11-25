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
