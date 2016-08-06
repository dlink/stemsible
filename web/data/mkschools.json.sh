# depricated script
# see Schools.genTypeAheadData()

dsdb='mysql -ustemsible -p$STEM_DBPASS -hlocalhost --database=dev_stemsible --local-infile=1'

echo 'select name from  schools'| $dsdb | \
   grep -v ^name$|sed -e 's/^/"/' -e 's/$/",/' | \
   flatten | \
   sed -e "s/^/[/" -e "s/, $/]/"
