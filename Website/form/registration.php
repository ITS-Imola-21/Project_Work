<?php
// Start a session if not already started
if (!session_id()) session_start();
ini_set('display_errors', 'Off');

$first_name = $_POST['first_name'];
$last_name = $_POST['last_name'];
$amazon_user = $_POST['amazon_user'];
$amazon_email = $_POST['amazon_email'];
$installation_date = $_POST['installation_date'];
$device_mac = $_POST['device_mac'];

$table_installations = 'table_installations';
$table_amazon_users = 'table_amazon_users';
$table_people = 'table_people';

$servername = "servername";
$username = "username";
$password = "password";
$db_name = "db_name";

if (isset($_POST['submit'])) {
    try {
        $conn = new PDO("mysql:host=$servername;dbname=$db_name", $username, $password);
        // Set the PDO error mode to exception
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        // Insert into the people table
        $insert_people = "INSERT INTO $table_people (first_name, last_name) VALUES ('$first_name','$last_name')";
        $conn->exec($insert_people);
        // Select the fk_id_person from the people table
        $stmt_people = $conn->prepare("SELECT id_person FROM $table_people WHERE last_name='$last_name'");
        // Execute the query
        $stmt_people->execute();
        $stmt_people->setFetchMode(PDO::FETCH_ASSOC);
        // Get the result of the select 
        while ($row_people = $stmt_people->fetch()) {
            $id_person = $row_people['id_person'];
            // Insert into the amazon_users table
            $insert_amazon_users = "INSERT INTO $table_amazon_users (amazon_user, amazon_email, fk_id_person) VALUES ('$amazon_user','$amazon_email','$id_person')";
            $conn->exec($insert_amazon_users);
            // Select the id_amazon_user from the amazon_users table
            $stmt_amazon_user = $conn->prepare("SELECT id_amazon_user FROM $table_amazon_users WHERE fk_id_person='$id_person'");
            // Execute the query
            $stmt_amazon_user->execute();
            $stmt_amazon_user->setFetchMode(PDO::FETCH_ASSOC);
            // Get the result of the select 
            $row_amazon_user = $stmt_amazon_user->fetch();
            $id_amazon_user = $row_amazon_user['id_amazon_user'];
            $token = generateRandomString();
            // Insert into the installations table
            $insert_installations = "INSERT INTO $table_installations (installation_date, device_mac, token, fk_id_person, fk_id_amazon_user) VALUES ('$installation_date', '$device_mac', '$token', '$id_person', '$id_amazon_user')";
            $conn->exec($insert_installations);
            // Retrieve the token and display it
            $stmt_token = $conn->prepare("SELECT token FROM $table_installations WHERE fk_id_person='$id_person'");
            $stmt_token->execute();
            $stmt_token->setFetchMode(PDO::FETCH_ASSOC);
            // Get the result of the select 
            $row_token = $stmt_token->fetch();
            $token_from_table = $row_token['token'];
            ?>
            <div class="alert alert-success" role="alert">
                <h4 class="alert-heading">Registered!</h4>
                <p>Everything went well, your access token is <?=$token_from_table?>, please remember it!</p>
            </div>
            <?php
            //echo "Everything went well, your access token is " ."$token_from_table" . " ". "Please remember it!";
        }
    } catch (PDOException $e) {
        echo "Connection failed: " . $e->getMessage();
    }
    $conn = null;
}

function generateRandomString($length = 10) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[random_int(0, $charactersLength - 1)];
    }
    return $randomString;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="script.js"></script>
</head>
<body>
<div class="container mt-5 w-75">
    <div class="row">
        <div class="col-md-6 offset-md-3">
            <div class="mb-3">
                <h3>Register</h3>
            </div>
            <div class="mb-3">
                <h6>This page's functionality has been disabled for security reasons.</h6>
            </div>
            <form action="#" method="post" class="shadow p-4 border border-primary rounded bg-white ">
                <div class="mb-3 ">
                    <label for="first_name"><b>First Name</b></label>
                    <input type="text" class="form-control border border-primary" name="first_name" id="first_name" placeholder="First Name" required>
                </div>

                <div class="mb-3">
                    <label for="last_name">Last Name</label>
                    <input type="text" class="form-control border border-primary" name="last_name" id="last_name" placeholder="Last Name" required>
                </div>

                <div class="mb-3">
                    <label for="amazon_email">Amazon Email</label>
                    <input type="text" class="form-control border border-primary" name="amazon_email" id="amazon_email" placeholder="Email" required>
                </div>

                <div class="mb-3">
                    <label for="amazon_user">Amazon User</label>
                    <input type="text" class="form-control border border-primary" name="amazon_user" id="amazon_user" placeholder="User" required>
                </div>
                <div class="mb-3">
                    <label for="device_mac">Device MAC address</label>
                    <input type="text" class="form-control border border-primary" name="device_mac" id="device_mac" placeholder="MAC" required>
                </div>
                <div class="mb-3">
                    <label for="installation_date">Installation Date</label>
                    <input type="date" class="form-control border border-primary" name="installation_date" id="installation_date" placeholder="Date" required>
                </div>

                <div class="mb-3">
                    <button type="submit" class="btn btn-primary border border-primary" name="submit" value="submit">Submit</button>
                </div>
            </form>
        </div>
    </div>
</div>
</body>
</html>
