<?php
header("Access-Control-Allow-Origin: *");

$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "recognition";

try
{
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    // set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // prepare sql and bind parameters
    $stmt = $conn->prepare("SELECT username, password FROM users
                            WHERE username = :username AND password = :password ");
    $stmt->bindParam(':username', $_GET['username']);
    $stmt->bindParam(':password', $_GET['password']);
    $stmt->execute();

    if($stmt->fetch())
    {
        $response['Success'] = "Welcome";
        echo json_encode($response);
    }
    else
    {
      // code...
      echo 'Rien';
    }
}
catch(PDOException $e)
{
   //$donnee['error'] = "Erreur";
   //echo json_encode($donnee);
   echo "Error: " . $e->getMessage();
}
$conn = null;
?>
