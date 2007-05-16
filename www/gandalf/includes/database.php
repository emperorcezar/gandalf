<?php

function connectToDatabase()
{
	$link = mysql_connect('localhost','gandalf','astari') or die('ERROR: '.mysql_error());
	mysql_select_db('gandalf');
	return $link;

}

?>