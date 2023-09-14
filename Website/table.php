<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telemetries</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="script.js">
</script>
</head>
<body>
<nav class="navbar navbar-expand-sm">
        <div class="container-fluid">
          <ul class="nav nav-pills ">
            <li class="nav-item">
              <a class="nav-link text-white" href="index.html">Home</a>
            </li>
            <li class="nav-item px-2">
              <a class="nav-link text-white" href="chi_siamo.html">About Us</a>
            </li>
            <li class="nav-item  px-2">
              <a class="nav-link text-white" href="cloud.html">Cloud</a>
            </li>
            <li class="nav-item  px-2">
              <a class="nav-link text-white" href="iot.html">IoT</a>
            </li>
            <li class="nav-item  px-2">
              <a class="nav-link text-white" href="networking.html">Networking</a>
            </li>
            <li class="nav-item  px-2">
              <a class="nav-link text-white" href="sito_web.html">Website</a>
            </li>
            <li class="nav-item  px-2">
              <a class="nav-link text-white" href="#">Telemetries</a>
            </li>
            <li class="nav-item px-2">
              <a href="https://www.fitstic.it/it/b/5494/tecnico-superiore-per-la-progettazione-di-infrastrutture-e-la-gestione">
                <img src="images/Imola.png" style="width: 8%;" > 
              </a> 
            </li>
          </ul>   
        </div>

      </nav>
      <header>
        <p class="h1">Telemetries</p>
      </header>
      <div class="container-fluid  px-xxl-5 py-5 d-flex w">
        <div class="box-content">
            <!-- container per il testo -->
            <div class="p-2 flex-grow-1">
                <h1 class="title">Data visualization</h1>
                <h5 class="subtitle">
                On this page, you can view the telemetry data from Arduino in response to a request sent by the Echo Dot.
                </h5>
                <div></div>
            </div>
            </div>
        </div>

    </div>
      <div class=" d-flex justify-content-center gray-container flex-column" style="padding:5%; overflow-x:auto;">

<?php
// Connect to database
$servername = "servername";
$username = "username";
$password = "password";
$db_name = "db_name";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$db_name", $username, $password);
    // Set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}

// Determine the total number of rows in the table
$count_query = "SELECT COUNT(*) FROM my_event_view";
$count_result = $conn->query($count_query);
$total_rows = $count_result->fetchColumn();

// Define the number of rows to display per page
$rows_per_page = 10;

// Determine the current page number
if (isset($_GET['page'])) {
    $current_page = $_GET['page'];
} else {
    $current_page = 1;
}

// Calculate the offset for the SQL query
$offset = ($current_page - 1) * $rows_per_page;

// Select the rows to display for the current page
$select_query = "SELECT id_evento, data_time, valore_effetto, descrizione, descrizione_tipo_misura FROM my_event_view order by data_time DESC LIMIT $offset, $rows_per_page ";
$select_result = $conn->query($select_query);

?>
<div class="d-flex justify-content-center">
    <table id="dtHorizontalExample" class="table table-bordered justify-content-center" style="width:80%">
        <thead class="thead-dark" style="background-color:#3776ab;color:white" id="table">
            <tr class='text-center'>
                <th scope="col">Request</th>
                <th scope="col">Date</th>
                <th scope="col">Value</th>
                <th scope="col">Measurement type</th>
                <!-- <th scope="col">Tipo misura</th> -->
            </tr>
        </thead>
        <tbody>
            <?php foreach ($select_result as $row) { 
                $row['valore_effetto'] = round($row['valore_effetto'], 2);?>
                <tr>
                    <td style='width:150px;border:1px solid black;'><?php echo $row['descrizione']; ?></td>
                    <td style='width:150px;border:1px solid black;'><?php echo $row['data_time']; ?></td>
                    <td style='width:150px;border:1px solid black;'><?php echo $row['valore_effetto']; ?></td>
                    <!-- <td style='width:150px;border:1px solid black;'></td> -->
                    <td style='width:150px;border:1px solid black;'><?php echo $row['descrizione_tipo_misura']; ?></td>
                </tr>
            <?php } ?>
        </tbody>
    </table>
</div>
<?php

// Display pagination links with Bootstrap styles
$num_pages = ceil($total_rows / $rows_per_page);
if ($current_page > 1 || $current_page < $num_pages) {
    echo "<nav class=\"bg-transparent \"><ul class=\"pagination justify-content-center \">";
    if ($current_page > 1) {
        echo "<li class=\"page-item\"><a class=\"page-link\" href=\"?page=" . ($current_page - 1) . "#table\">Previous</a></li>";
    }
    if ($current_page < $num_pages) {
        echo "<li class=\"page-item\"><a class=\"page-link\" href=\"?page=" . ($current_page + 1) . "#table\">Next</a></li>";
    }
    echo "</ul></nav>";
}
?>

</div>
<footer class="text-center text-lg-start text-muted">
    <section>
      <div class="container text-center text-md-start mt-5">
        <div class="row mt-3">

          <!-- Fitstic first column footer-->
          <div class="col-md-3 col-lg-4 col-xl-3 mx-auto mb-4">
            <h6 class="text-uppercase fw-bold mb-4">FITSTIC</h6>
            <p>
              Fondazione Istituto Tecnico Superiore
              Tecnologie e Industrie Creative
            </p>
            <p>P.le Macrelli 100 - 47521 Cesena (FC)</p>
          </div>

          <!--Fitstic Logo, second column footer-->
          <div class="col-md-2 col-lg-2 col-xl-2 mx-auto mb-4  d-flex align-items-center justify-content-center">
            <p>
              <a href="https://www.fitstic.it/">
                <img src="images/logo_fitstic_bianco.jpg" style="width: 150px;" > 
              </a> 
            </p>
          </div>

          <!-- ITS Imola Logo third column footer-->
          <div class="col-md-3 col-lg-2 col-xl-2 mx-auto mb-4 d-flex align-items-center justify-content-center">
            <p>
              <a href="https://www.fitstic.it/it/b/5494/tecnico-superiore-per-la-progettazione-di-infrastrutture-e-la-gestione">
                <img src="images/Imola.png" style="width: 150px;" > 
              </a> 
            </p>
          </div>

          <!-- Contact fourth column footer-->
          <div class="col-md-4 col-lg-3 col-xl-3 mx-auto mb-md-0 mb-4">
            <h6 class="text-uppercase fw-bold mb-4">Contact</h6>
            <p>
              info@fitstic.it
            <br>
              www.fitstic.it
            </p>
            <div>+39 051 4858036-37</div>
          </div>

        </div>
      </div>
    </section>
  </footer>
</body>
</html>