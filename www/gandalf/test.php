<?php
require_once('includes/database.php');

connectToDatabase();

$insert = '"or 1=1 /*';

$sql = 'select * from commands where type = "'.$insert.'"';

$result = mysql_query($sql) or die(mysql_error());
print $result;

while($row = mysql_fetch_assoc($result))
{
	print "in row";
	print_r($row);
}
?>