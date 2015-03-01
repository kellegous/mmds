CFLAGS=-Wall -std=c++11
LDFLAGS=-lz -lpthread

OBJS=util.o status.o pagerank.o
BINS=cpagerank gpagerank

ALL: $(OBJS) $(BINS)

%.o: %.cc %.h
	clang++ -O3 $(CFLAGS) -c -o $@ $<

cpagerank: $(OBJS) pagerank.o
	clang++ -O3 $(LDFLAGS) -o $@ $^

gpagerank: pagerank.go $(OBJS)
	go build -o $@ $<

clean:
	rm -f $(OBJS) $(BINS)
