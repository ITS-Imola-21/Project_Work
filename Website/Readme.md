# PHP Database Interaction Script

**Table of Contents**
- [Website](#website)
- [Introduction](#introduction)
- [Usage](#usage)
- [Code Overview](#code-overview)
  - [Session Handling](#session-handling)
  - [Error Handling](#error-handling)
  - [JSON Data Decoding](#json-data-decoding)
  - [Database Configuration](#database-configuration)
  - [Database Connection](#database-connection)
  - [Data Processing](#data-processing)
  - [Database Queries](#database-queries)
  - [Error Handling (Exception Handling)](#error-handling-exception-handling)
  - [Connection Closing](#connection-closing)
- [Configuration](#configuration)
- [Security Considerations](#security-considerations)
- [Notes](#notes)
- [Credits](#credits)

## Website

You can access the project's goals and documentation by following this link: https://pw2023.itsimola.it/

## Introduction 

This PHP script is designed to interact with a MySQL database and handle incoming JSON data. Its primary purpose is to receive JSON data from an external source, decode it, and perform various operations within the database. The script ensures the authenticity of the data by verifying tokens.

## Usage

To use this script, you need to send JSON data to it via an HTTP request. Ensure that your JSON data includes the required fields, such as `amazon_email`, `token`, and other relevant data, as specified in the code. The script will handle the rest, interacting with the database as needed.

## Code Overview 

### Session Handling 

The script checks whether a PHP session is active and starts one if not already initiated.

### Error Handling 

PHP error display is turned off (`'Off'`) to prevent error messages from being shown to users.

### JSON Data Decoding 

The script reads JSON data from the request body using `file_get_contents` and decodes it into a PHP associative array (`$data`) using `json_decode`. This array contains the parsed JSON data for further processing.

### Database Configuration 

Configuration parameters for the database connection, including the server name, username, password, and database name, are set in this section. Ensure that you replace placeholder values with your actual database connection information.

### Database Connection

A PDO (PHP Data Objects) connection to the MySQL database is established. PDO provides a secure and efficient way to interact with databases.

### Data Processing 

Specific values from the decoded JSON data are assigned to variables for later use. These values typically include user information, installation data, event details, causes, and measurement information.

### Database Queries

A series of database queries are executed using PDO prepared statements to achieve the following:
   
   1. Retrieve `fk_id_person` from the `table_amazon_accounts` table based on the provided `amazon_email`.
   
   2. Retrieve the `token` from the `table_installations` table associated with the user identified by `fk_id_person`.
   
   3. Verify that the provided `token` matches the one stored in the database.
   
   4. Retrieve the `id_installation` associated with the user.
   
   5. Insert data into the `table_events` table, including `date_time`, `fk_id_installation`, `fk_id_cause`, `effect_value`, `log`, and `fk_id_measurement_type`.

### Error Handling (Exception Handling) 

The code includes exception handling using a try-catch block. If an error occurs during database connection or query execution, it catches the exception and displays an error message.

### Connection Closing

After all database operations are complete, the script closes the database connection.

## Configuration 

Please replace placeholder values such as `servername`, `username`, `password`, and `db_name` in the code with your actual database connection information.

## Security Considerations

This code is a basic example and may require further security enhancements, such as input validation and SQL injection prevention, depending on your specific use case and security requirements. Ensure that you follow best practices for securing database connections and handling sensitive data.

## Notes

This README provides an overview of the PHP script's functionality and usage. Be sure to adapt the code to your specific requirements and consider additional security measures based on your application's needs.

## Credits

- Federico Pattuelli
- Dahryl Ramirez
- Chiara Kularatna Diyagama Liyanage
- Alessandro Signorile
