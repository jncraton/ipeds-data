.PHONY: all clean

.SECONDARY: 

all: data/index.html

data/index.html: data/comparison.tsv
	cd data && python3 ../list_dir.py > index.html

data/comparison.tsv: data/ADM2016.zip data/ADM2016_Dict.zip data/SAL2016_IS.zip data/SAL2016_IS_Dict.zip data/SAL2016_NIS.zip data/SAL2016_NIS_Dict.zip y2016 y2015 y2014 y2013 y2012 y2011 y2010 y2009 y2008 y2007 y2006 y2005 ay1516 ay1415 ay1314 ay1213 ay1112 ay1011 ay0910 ay0809 ay0708 ay0607 ay0506 py2016 py2015 py2014 py2013 py2012 py2011 py2010 py2009 py2008 py2007 py2006 py2005
	python3 gen_comparison.py

y%: data/EF%A.zip data/EF%A_Dict.zip data/EF%B.zip data/EF%B_Dict.zip data/EF%C.zip data/EF%C_Dict.zip data/EF%D.zip data/EF%D_Dict.zip data/EAP%.zip data/EAP%_Dict.zip data/IC%.zip data/IC%_Dict.zip data/IC%_AY.zip data/IC%_AY_Dict.zip data/EFFY%.zip data/EFFY%_Dict.zip data/EFIA%.zip data/EFIA%_Dict.zip data/HD%.zip data/HD%_Dict.zip ;

py%: data/FLAGS%.zip data/FLAGS%_Dict.zip ;

ay%: data/SFA%.zip data/SFA%_Dict.zip data/F%_F1A.zip data/F%_F1A_Dict.zip data/F%_F2.zip data/F%_F2_Dict.zip data/F%_F3.zip data/F%_F3_Dict.zip ;

data/%.zip:
	wget https://nces.ed.gov/ipeds/datacenter/$@ --quiet -O $@
	unzip -q -d data $@
	rm -f $@

clean:
	rm -f data/*
