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
    $presence = "1";
    $stmt = $conn->prepare("UPDATE person SET presence = :presence, datePresence = :datePresence 
                            WHERE id = :id;");
    
    $stmt->bindParam(':presence', $presence);
    $stmt->bindParam(':datePresence', date("Y-m-d H:i:s"));
    //echo $_POST['id'];
    $stmt->bindParam(':id', $_POST['id']);
   
   
    $stmt->execute();

    echo "Success";
}
catch(PDOException $e)
{
    echo "Error: " . $e->getMessage();
}
$conn = null;
?>
