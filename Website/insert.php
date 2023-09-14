<?php
// Start a session if not already started
if (!session_id()) session_start();
ini_set('display_errors', 'Off');

// Get the JSON data sent to me and decode it
$data = json_decode(file_get_contents('php://input'), true);

// Access the values using the variable $data

// Table: table_people
$table_people = 'table_people';
$name = $_POST['name'];

// Table: table_amazon_accounts
$table_amazon_accounts = 'table_amazon_accounts';
$amazon_user = $data['amazon_user'];
$amazon_email = $data['amazon_email'];

// Table: table_installations
$table_installations = 'table_installations';
$installation_date = $data['installation_date'];
$device_mac = $data['device_mac'];
$token = $data['token'];

// Table: table_events
$table_events = 'table_events';
$date_time = $data['date_time'];
$effect_value = $data['effect_value'];
$log = $data['log'];

// Table: table_causes
$table_causes = 'table_causes';
$cause_id = $data['cause_id'];
$value_type = $data['value_type'];

// Table: table_measurement
$table_measurement = "table_measurement";
$measurement_id = $data['measurement_id'];

$servername = "servername";
$username = "username";
$password = "password";
$db_name = "db_name";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$db_name", $username, $password);
    // Set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Select fk_id_person from the amazon_accounts table
    $stmt_amazon_user = $conn->prepare("SELECT fk_id_person FROM $table_amazon_accounts WHERE amazon_email='$amazon_email'");
    // Execute the query
    $stmt_amazon_user->execute();
    $stmt_amazon_user->setFetchMode(PDO::FETCH_ASSOC);

    // Get the result of the select
    while ($row_amazon_user = $stmt_amazon_user->fetch()) {
        $person_id = $row_amazon_user['fk_id_person'];

        // Retrieve the token
        $stmt_token_installations = $conn->prepare("SELECT token FROM $table_installations WHERE fk_id_person='$person_id'");
        $stmt_token_installations->execute();
        $stmt_token_installations->setFetchMode(PDO::FETCH_ASSOC);
        $row_token_installations = $stmt_token_installations->fetch();
        $token_from_table = $row_token_installations['token'];

        // Check if the token in the URL matches the token in the database
        if ($token == $token_from_table) {

            // Retrieve the installation_id
            $stmt_installations = $conn->prepare("SELECT id_installation FROM $table_installations WHERE fk_id_person='$person_id'");
            $stmt_installations->execute();
            $stmt_installations->setFetchMode(PDO::FETCH_ASSOC);
            $row_id_installation = $stmt_installations->fetch();
            $installation_id = $row_id_installation['id_installation'];

            // Insert into the events table
            $insert_events = "INSERT INTO $table_events (date_time, fk_id_installation, fk_id_cause, effect_value, log, fk_id_measurement_type) VALUES ('$date_time','$installation_id','$cause_id', '$effect_value', '$log', '$measurement_id')";
            $conn->exec($insert_events);
        }
    }
} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
$conn = null;
?>
