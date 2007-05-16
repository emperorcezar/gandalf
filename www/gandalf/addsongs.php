<?
require_once('includes/error.inc.php');
require_once('includes/id3.class.php');
require_once('includes/database.php');
require_once('includes/getid3/audioinfo.class.php');

#Got me some variables to later be used as global
$song_paths = Array();
$song_matrix = Array();





function getSongPaths()
{
	global $song_paths;
	
	$query = 'SELECT path FROM files';
	$result = mysql_query($query) or die('Query failed: ' . mysql_error());
	
	
	
	while($row = mysql_fetch_assoc($result))
	{
		$song_paths[] = $row["path"];
	}
}

function findUnlistedSongs($path)
{
	global $song_paths;
	global $with_tags;
	global $no_tags;
	global $song_matrix;
	
	$song_data = Array();
	
	$handle = opendir($path);
	
	while (false !== ($file = readdir($handle))) 
	{
		if( is_dir($path.$file) && $file != '.' && $file != '..' )
		{
			findUnlistedSongs($path.$file.'/');
			#echo "Going into Directory: ".$path.$file."<br/>";
		
		}
		else if(fnmatch("*.mp3",$file))
		{
			if(!in_array($path.$file,$song_paths))
			{
				
				$myId3 = new AudioInfo();
				if (false != ($info = $myId3->Info($path.$file)))
				{
					
					/*
					$query = 'INSERT INTO files (artist,title,album,path) VALUES("'.$myId3->getArtist().'","'.$myId3->getTitle().'","'.$myId3->getAlbum().'","'.$path.$file.'")';
					echo $query.'<br/>';
					mysql_query($query);
					*/
					#Get the length
					
					
					
					
					
					$song_data['artist'] = $info['tags']['id3v2']['artist'][0];
					$song_data['title'] = $info['tags']['id3v2']['title'][0];
					$song_data['album'] = $info['tags']['id3v2']['album'][0];
					$song_data['path'] = $path.$file;
					$song_data['comment'] = $info['tags']['id3v2']['comment'][0];
					$song_data['genre'] = $info['tags']['id3v2']['genre'][0];
					$song_data['length'] = floor($info['playing_time']);
					
					#$song_data["length"] = $seconds;
					$song_matrix[] = $song_data;
					echo "Found song: ".$song_data["path"].'<br />';
					
					$mp3 = null;
					$myId3 = null;
				
					
				}
			
			}
			else
			{
				echo 'Song is in database: '.$path.$file.'<br />';
				/*
				$mp3 = new MP3($path.$file);
				$mp3->get_info();
				
				$timearray = explode(':',$mp3->info["length"]);
				$seconds = $timearray[0]*60+$timearray[1];
				echo $seconds.'<br />'.'BITRATE: '.$mp3->info["bitrate"].'<br />';
				*/
			}
			
		}
	}
	closedir($handle);

}


$path = '/home/cezar/mp3/';

$link = connectToDatabase();
getSongPaths();




findUnlistedSongs($path);

foreach ($song_matrix as $song)
{
	if($song["artist"] != '' && $song["title"] != '')
	{
		$query = 'INSERT INTO files (artist,title,album,comment,length,path) VALUES("'.$song["artist"].'","'.$song["title"].'","'.$song["album"].'","'.$song["comment"].'","'.$song["length"].'","'.$song["path"].'")';
		#echo $query.'<br/>';
		mysql_query($query) or die('Query failed: ' . mysql_error());
		
		$query = 'INSERT INTO genres (id,genre) VALUES("'.mysql_insert_id($link).'","'.$song["genre"].'")';
		#echo $query.'<br/>';
		mysql_query($query) or die('Query failed: ' . mysql_error());
		
	}
}



?>