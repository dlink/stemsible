dsdb='mysql -ustemsible -predXnapper56 -hlocalhost --database=dev_stemsible --local-infile=1'

echo 'select name from  schools'| $dsdb | \
   grep -v ^name$|sed -e 's/^/"/' -e 's/$/",/' | \
   flatten | \
   sed -e "s/^/[/" -e "s/, $/]/"
