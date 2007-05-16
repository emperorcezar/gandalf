<?php
    
    require_once('error.inc.php');
    require_once('id3.class.php');
    
    $nome_arq  = '/home/cezar/Enya.mp3';
	 $myId3 = new ID3($nome_arq);
	 if ($myId3->getInfo()){
         echo('<HTML>');
         echo('<a href= "'.$nome_arq.'">Clique para baixar: </a><br>');
         echo('<table border=1>
               <tr>
                  <td><strong>Artist</strong></td>
                  <td><strong>Title</strong></font></div></td>
                  <td><strong>Track</strong></font></div></td>
                  <td><strong>Album</strong></font></div></td>
                  <td><strong>Genre</strong></font></div></td>
                  <td><strong>Comments</strong></font></div></td>
               </tr>
               <tr>
                  <td>'. $myId3->getArtist() . '&nbsp</td>
                  <td>'. $myId3->getTitle()  . '&nbsp</td>
                  <td>'. $myId3->getTrack()  . '&nbsp</td>
                  <td>'. $myId3->getAlbum()  . '&nbsp</td>
                  <td>'. $myId3->getGenre() . '&nbsp</td>
                  <td>'. $myId3->tags['COMM']. '&nbsp</td>
               </tr>
            </table>');
         echo('</HTML>');
   	}else{
    	echo($errors[$myId3->last_error_num]);
   }
   
?>
