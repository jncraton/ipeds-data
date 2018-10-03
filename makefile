.PHONY: all clean

.SECONDARY: 

all: y2017 y2016 y2015 y2014 y2013 y2012 y2011 y2010 y2009 y2008 y2007 y2006 y2005

y%: data/EFFY%.csv data/HD%.csv ;

# https://nces.ed.gov/ipeds/datacenter/datafiles.aspx
data/%.zip:
	wget https://nces.ed.gov/ipeds/datacenter/$@ --quiet -O $@

data/%.csv: data/%.zip
	unzip $< -d data
	rm $<

clean:
	rm -f data/*
