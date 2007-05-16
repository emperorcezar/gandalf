<?php
require_once('includes/database.php');
require_once('includes/commands.php');


connectToDatabase();

if(isset($_GET["action"]))
	{
		if(isset($_POST["start"]))
		{
			startGandalf();
		}
		if(isset($_POST["stop"]))
		{
			stopGandalf();
		}
	}
	else
	{
?>
<html>
	<head>
		<title>Control Gandalf</title>
	</head>
	<body>
	
		<form action="<?php echo $_SERVER["PHP_SELF"] ?>?action=command" method="post" name="start">
			<input type="submit" name="start" class="button" value="Start System" />
		</form>

		<form action="<?php echo $_SERVER["PHP_SELF"] ?>?action=command" method="post" name="stop">
			<input type="submit" name="stop" class="button" value="Stop System" />
		</form>	
	</body>
</html>
<?php
}
?>