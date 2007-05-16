<?php

function startGandalf()
{
/* This function starts the gandalf system from a stopped status */
	$query = 'UPDATE commands SET switch="1" where type = "0"';
	$result = mysql_query($query) or die('Query failed: ' . mysql_error());
	echo "Gandalf Started";
}

function stopGandalf()
{
/*This function stops the gandalf system from a started status */
	$query = 'UPDATE commands SET switch="0" where type = "0"';
	$result = mysql_query($query) or die('Query failed: ' . mysql_error());
	echo "Gandalf Stopped";
}

?>