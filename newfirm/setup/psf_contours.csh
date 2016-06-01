#create listing of skysub files
set prefix = `echo $cwd | awk 'BEGIN{FS="/"} {print $NF}'`
awk 'BEGIN{FS="."} {sub(/raw\//, ""); print $0 ".fits", $NF}' < raw.lis > $prefix.sub.lst

idl psf_contours.idl >& psf_contours.log

#updated PS_syntax
set file = ${prefix}.psf
awk '{if($1=="$IDL_DICT"){printf("$IDL_DICT begin 20 774 translate 0.0283465 dup scale 270 rotate MITERLIMIT\n")} else{print}}' < $file.eps > test.eps
mv test.eps $file.eps
ps2pdf13 $file.eps $file.pdf

awk '{if($1=="end"){printf("showpage\nend\n")} else{print}}' < $file.eps > test.eps
mv test.eps $file.eps
ps2pdf13 $file.eps $file.pdf

#mkdir psf
#mv *.cat psf
#mv *.mag psf
#mv *psf.fits psf
