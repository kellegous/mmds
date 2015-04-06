package main

import (
	"archive/zip"
	"bufio"
	"bytes"
	"flag"
	"fmt"
	"io"
	"log"
	"runtime"
	"time"
	"unsafe"
)

var space = []byte{' '}

// A structure that allows us to turn words into "atoms" where
// an atom is just a uint32 identifier of that word and sentences
// can, therefore, be represented as an ordered list of uint32s.
type Atomizer struct {
	w map[string]uint32
	i uint32
}

// Atomize a single word.
func (a *Atomizer) Atom(word []byte) uint32 {
	w := string(word)
	if v, has := a.w[w]; has {
		return v
	}

	v := a.i
	a.w[w] = v
	a.i++
	return v
}

// Atomize a whole sentence.
func (a *Atomizer) Atoms(words [][]byte) []uint32 {
	n := len(words)
	ats := make([]uint32, n)
	for i := 0; i < n; i++ {
		ats[i] = a.Atom(words[i])
	}
	return ats
}

// Represents a unique sentence in the data that holds both the atoms
// that make up its content and a count for the number of times it
// appears in the data.
type Sentence struct {
	words []uint32
	count int
}

// An Idx key structure that consists of a head hash (a), a tail hash (b)
// and the length of the sentence (n).
type IdxEnt struct {
	a uint64
	b uint64
	n uint32
}

// The index structure keyed on our head/tail/length LSH scheme.
type Idx struct {
	head map[IdxEnt][]*Sentence
	tail map[IdxEnt][]*Sentence
	all  []*Sentence
}

func NewIdx() *Idx {
	return &Idx{
		head: map[IdxEnt][]*Sentence{},
		tail: map[IdxEnt][]*Sentence{},
	}
}

// Simple function to determine if two sentences are identical.
func WordsAreEqual(a, b []uint32) bool {
	la, lb := len(a), len(b)
	if la != lb {
		return false
	}

	for i := 0; i < la; i++ {
		if a[i] != b[i] {
			return false
		}
	}

	return true
}

// Add the list of atoms to the index as a sentence. This will
// either construct a new Sentence, or update the count on an
// existing instance.
func (x *Idx) Add(s []uint32) {
	m := len(s)

	// To find any existing entry, we're only going to depend on the
	// head part of the index, so compute the key for the head.
	he := IdxEnt{
		a: uint64(s[0]<<32) | uint64(s[1]),
		b: uint64(s[2]<<32) | uint64(s[3]),
		n: uint32(m),
	}

	// Do a simple linear search of the head index looking for an
	// exact match.
	for _, sc := range x.head[he] {
		if WordsAreEqual(s, sc.words) {
			sc.count++
			return
		}
	}

	// If we didn't find it, we'll just proceed with creating a new
	// Sentence and putting it in the head and tail indexes.
	sent := &Sentence{
		words: s,
		count: 1,
	}

	x.head[he] = append(x.head[he], sent)

	te := IdxEnt{
		a: uint64(s[m-2]<<32) | uint64(s[m-1]),
		b: uint64(s[m-4]<<32) | uint64(s[m-3]),
		n: uint32(m),
	}
	x.tail[te] = append(x.tail[te], sent)

	x.all = append(x.all, sent)
}

// Compute the number of binary combinations for N items. To do this we need
// to sum 1 + 2 + 3 + ... + (n -1). This kind of ends up being the same as
// computing the area of a n x (n-1) triangle, so we get n*(n-1)/2.
func NChoose2(n int) int {
	if n < 2 {
		return 0
	}
	return n * (n - 1) >> 1
}

// Compute the number of pairs in the index that have a edit distance that
// is <= 1. This implementation divides the search space into W stripes where
// W is the number of CPUs driving the runtime.
func (x *Idx) CountPairs() int {
	sns := x.all

	// number of workers
	w := runtime.NumCPU()

	// create a channel for each worker
	ch := make(chan int, w)

	// compute the number of items each worker
	// will do.
	n := len(sns)
	if w > 1 {
		n /= (w - 1)
	}

	for len(sns) > n {
		go x.countPairs(ch, sns[:n])
		sns = sns[n:]
	}
	x.countPairs(ch, sns)

	c := 0
	for i := 0; i < w; i++ {
		c += <-ch
	}
	return c
}

// A helper method for CountPairs, this carries out the actual counting
// on a slice of the search space.
func (x *Idx) countPairs(ch chan int, sns []*Sentence) {
	c := 0

	head, tail := x.head, x.tail

	for i, n := 0, len(sns); i < n; i++ {
		s := sns[i]
		m := len(s.words)
		mm := uint32(m)
		ha := uint64(s.words[0]<<32) | uint64(s.words[1])
		hb := uint64(s.words[2]<<32) | uint64(s.words[3])
		ta := uint64(s.words[m-2]<<32) | uint64(s.words[m-1])
		tb := uint64(s.words[m-4]<<32) | uint64(s.words[m-3])

		c += NChoose2(s.count)

		ents := [][]*Sentence{
			head[IdxEnt{ha, hb, mm}],
			head[IdxEnt{ha, hb, mm - 1}],
			head[IdxEnt{ha, hb, mm + 1}],
			tail[IdxEnt{ta, tb, mm}],
			tail[IdxEnt{ta, tb, mm - 1}],
			tail[IdxEnt{ta, tb, mm + 1}],
		}

		ps := uintptr(unsafe.Pointer(s))

		seen := map[*Sentence]bool{}
		for _, ent := range ents {
			for _, sc := range ent {

				// This unsafe pointer trick is just a hack around the fact that the
				// pairs (A, B) and (B, A) are the same and should not be double counted.
				// We only consider pairs where the "greater" element is first and the
				// notion of greater just needs to be consistent, so we use the pointer
				// value itself. Similarly, the "equals" part just eliminates the pair
				// (A, A).
				if ps >= uintptr(unsafe.Pointer(sc)) || seen[sc] {
					continue
				}

				seen[sc] = true

				if !HasSingleEditOrLess(s.words, sc.words) {
					continue
				}

				c += s.count * sc.count
			}
		}
	}

	ch <- c
}

func LoadSentences(r io.Reader) (*Idx, error) {
	var buf bytes.Buffer
	br := bufio.NewReader(r)

	atm := Atomizer{
		w: map[string]uint32{},
	}

	idx := NewIdx()

	wch, cch := make(chan []uint32, 100), make(chan bool)

	go func() {
		for s := range wch {
			idx.Add(s)
		}

		cch <- true
	}()

	for {
		b, p, err := br.ReadLine()
		if err == io.EOF {
			close(wch)
			<-cch
			return idx, nil
		} else if err != nil {
			return nil, err
		}

		buf.Write(b)
		if p {
			continue
		}

		line := buf.Bytes()
		wrds := atm.Atoms(bytes.Split(
			line[bytes.Index(line, space)+1:],
			space))
		wch <- wrds
		// idx.Add(wrds)
		buf.Reset()
	}
}

func LoadSentencesFromFile(filename string) (*Idx, error) {
	z, err := zip.OpenReader(filename)
	if err != nil {
		return nil, err
	}
	defer z.Close()

	if len(z.File) == 0 {
		return nil, fmt.Errorf("no files in %s", filename)
	}

	r, err := z.File[0].Open()
	if err != nil {
		return nil, err
	}
	defer r.Close()

	return LoadSentences(r)
}

func HasSingleEditOrLess(a, b []uint32) bool {
	lenA, lenB := len(a), len(b)
	diff := lenA - lenB
	if diff > 1 || diff < -1 {
		return false
	} else if diff == 0 {
		c := 0
		for i := 0; i < lenA; i++ {
			if a[i] != b[i] {
				c++
				if c > 1 {
					return false
				}
			}
		}
		return true
	} else {
		if lenA > lenB {
			a, b = b, a
			lenA, lenB = lenB, lenA
		}

		// shorter 1 is a
		c := 0
		for i := 0; i < lenA; i++ {
			if a[i] != b[i+c] {
				c++
				i--
				if c > 1 {
					return false
				}
			}
		}
		return true
	}
}

func main() {
	flagSrc := flag.String("src", "test.txt.zip", "the input file")
	flag.Parse()

	runtime.GOMAXPROCS(runtime.NumCPU())

	at := time.Now()
	idx, err := LoadSentencesFromFile(*flagSrc)
	if err != nil {
		log.Panic(err)
	}

	bt := time.Now()

	fmt.Printf("%d\n", idx.CountPairs())

	ct := time.Now()
	fmt.Printf("loading & indexing: %s, counting: %s, total: %s\n",
		bt.Sub(at),
		ct.Sub(bt),
		ct.Sub(at))
}
