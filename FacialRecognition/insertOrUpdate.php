<?php
$servername = "YOUR_HOSTNAME";
$username = "YOUR_USERNAME";
$password = "YOUR_PASSWORD";
$dbname = "YOUR_DATABASE_NAME";

try 
{
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    // set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // prepare sql and bind parameters
    $stmt = $conn->prepare("INSERT INTO person (nom, age, sexe, presence, datePresence) 
                            VALUES (:nom, :age, :sexe, :presence, :datePresence)");
    $stmt->bindParam(':nom', $_POST['nom']);
    $stmt->bindParam(':age', $_POST['age']);
    $stmt->bindParam(':sexe', $_POST['sexe']);
    $stmt->bindParam(':presence', $_POST['presence']);
    $stmt->bindParam(':datePresence', date("Y-m-d H:i:s"));

    $stmt->execute();

    echo "Success";
}
catch(PDOException $e)
{
    echo "Error: " . $e->getMessage();
}
$conn = null;
?>
