while read LINE
do echo $LINE | ete3 ncbiquery --info | sed -n 2p | cut -f 1 -d '	'
done < species.txt
