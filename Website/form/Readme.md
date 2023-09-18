# Registration System

This code is a registration system for collecting user information and storing it in a MySQL database. It is intended for educational purposes and can be used as a starting point for building a registration system for your web application.

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [Security Considerations](#security-considerations)

## Introduction

This PHP code creates a simple registration system that collects the following user information:

- First Name
- Last Name
- Amazon Email
- Amazon User
- Device MAC address
- Installation Date

The collected data is then inserted into three database tables: `table_people`, `table_amazon_users`, and `table_installations`. It also generates an access token for each registration.

## Requirements

Before using this code, make sure you have the following requirements in place:

1. PHP: Ensure that you have PHP installed on your web server.

2. MySQL Database: You'll need a MySQL database where the user information will be stored. Update the database connection details in the code as described in the setup section.

3. Bootstrap: The code uses Bootstrap for styling the HTML form. You can link to the Bootstrap CSS from a content delivery network (CDN) as shown in the code.

## Setup

Follow these steps to set up the registration system:

1. **Database Setup**: Create the necessary database tables in your MySQL database. You can use the following SQL statements as a reference:

   ```sql
   CREATE TABLE table_people (
       id_person INT AUTO_INCREMENT PRIMARY KEY,
       first_name VARCHAR(255) NOT NULL,
       last_name VARCHAR(255) NOT NULL
   );

   CREATE TABLE table_amazon_users (
       id_amazon_user INT AUTO_INCREMENT PRIMARY KEY,
       amazon_user VARCHAR(255) NOT NULL,
       amazon_email VARCHAR(255) NOT NULL,
       fk_id_person INT,
       FOREIGN KEY (fk_id_person) REFERENCES table_people(id_person)
   );

   CREATE TABLE table_installations (
       id_installation INT AUTO_INCREMENT PRIMARY KEY,
       installation_date DATE NOT NULL,
       device_mac VARCHAR(255) NOT NULL,
       token VARCHAR(255) NOT NULL,
       fk_id_person INT,
       fk_id_amazon_user INT,
       FOREIGN KEY (fk_id_person) REFERENCES table_people(id_person),
       FOREIGN KEY (fk_id_amazon_user) REFERENCES table_amazon_users(id_amazon_user)
   );
   ```

2. **Database Configuration**: Update the following variables in your PHP code with your database connection details:

   - `$servername`: The name of your MySQL server.
   - `$username`: Your MySQL username.
   - `$password`: Your MySQL password.
   - `$db_name`: The name of the database where the tables are created.

3. **Web Server**: Host your PHP code on a web server that supports PHP.

## Usage

1. Access the registration form by opening the PHP file in a web browser.

2. Fill in the required user information:
   - First Name
   - Last Name
   - Amazon Email
   - Amazon User
   - Device MAC address
   - Installation Date

3. Click the "Submit" button to register the user.

4. After successful registration, an access token is generated and displayed to the user on the webpage.

## Code Explanation

The code is structured as follows:

- It starts by setting up a PHP session and error handling.

- It collects user input from an HTML form.

- It establishes a connection to the MySQL database and inserts the user data into the `table_people`, `table_amazon_users`, and `table_installations` tables.

- It generates a random access token for each registration using the `generateRandomString` function.

- It displays a success message with the access token to the user.

## Security Considerations

This code provides a basic registration system and should not be used as-is in production without considering security implications. Here are some security considerations:

- **Input Validation**: Implement input validation to protect against SQL injection and other malicious inputs.

- **Password Hashing**: If you plan to collect passwords, use proper password hashing techniques.

- **Database Security**: Ensure proper database permissions and use prepared statements to prevent SQL injection.

- **Session Management**: Implement secure session management to protect against session hijacking.

- **Data Privacy**: Be aware of data privacy regulations like GDPR and ensure user consent and data protection.

- **Error Handling**: Improve error handling to provide more informative error messages without revealing sensitive information.

- **HTTPS**: Use HTTPS to encrypt data transmitted between the client and server.

- **Rate Limiting and CAPTCHA**: Implement rate limiting and CAPTCHA to prevent abuse and spam.

- **CSRF Protection**: Implement Cross-Site Request Forgery (CSRF) protection.

- **Code Review**: Have your code reviewed by security experts to identify vulnerabilities.

Remember that this code is a starting point and should be enhanced to meet the security requirements of your application.
