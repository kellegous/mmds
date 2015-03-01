CFLAGS=-Wall -std=c++11
LDFLAGS=-lz -lpthread

OBJS=util.o status.o pagerank.o
BINS=cpagerank gpagerank

URL=http://snap.stanford.edu/data/web-Google.txt.gz

ALL: $(OBJS) $(BINS) web-Google.txt.gz

web-Google.txt.gz:
	curl -O $(URL)
	
%.o: %.cc %.h
	clang++ -O3 $(CFLAGS) -c -o $@ $<

cpagerank: $(OBJS) pagerank.o
	clang++ -O3 $(LDFLAGS) -o $@ $^

gpagerank: pagerank.go $(OBJS)
	go build -o $@ $<

clean:
	rm -f $(OBJS) $(BINS)
