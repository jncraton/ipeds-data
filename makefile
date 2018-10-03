.PHONY: all clean

.SECONDARY: 

all: data/index.html

data/index.html: data/comparison.tsv
	cd data && python3 ../list_dir.py > index.html

data/comparison.tsv: y2017 y2016 y2015 y2014 y2013 y2012 y2011 y2010 y2009 y2008 y2007 y2006 y2005 ay1516 ay1415 ay1314 ay1213 ay1112 ay1011 ay0910 ay0809 ay0708 ay0607 ay0506 py2016 py2015 py2014 py2013 py2012 py2011 py2010 py2009 py2008 py2007 py2006 py2005
	python3 gen_comparison.py

y%: data/IC%.csv data/IC%_Dict.csv data/IC%_AY.csv data/IC%_AY_Dict.csv data/EFFY%.csv data/EFFY%_Dict.csv data/EFIA%.csv data/EFIA%_Dict.csv data/HD%.csv data/HD%_Dict.csv ;

py%: data/FLAGS%.csv data/FLAGS%_Dict.csv ;

ay%: data/SFA%.csv data/SFA%_Dict.csv ;

data/%.zip:
	wget https://nces.ed.gov/ipeds/datacenter/$@ --quiet -O $@

data/%.csv: data/%.zip
	unzip $< -d data
	rm $<

clean:
	rm -f data/*
