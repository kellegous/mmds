package main

import (
	"bufio"
	"bytes"
	"compress/gzip"
	"flag"
	"fmt"
	"io"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

type Rows struct {
	Rows []*Row
}

type Row struct {
	Vals []float64
	Dims []int
}

func (r *Rows) reserve(id int) {
	for id >= len(r.Rows) {
		r.Rows = append(r.Rows, &Row{})
	}
}

func (r *Rows) Add(frid int, toids []int) {
	n := len(toids)
	v := 1.0 / float64(n)
	r.reserve(frid)
	for i := 0; i < n; i++ {
		r.reserve(toids[i])
		row := r.Rows[toids[i]]
		row.Vals = append(row.Vals, v)
		row.Dims = append(row.Dims, frid)
	}
}

func DimFor(nameToDim map[int]int, dims *[]int, name int) int {
	eid, has := nameToDim[name]
	if has {
		return eid
	}

	eid = len(*dims)
	nameToDim[name] = eid
	*dims = append(*dims, name)
	return eid
}

func ReadMatrix(filename string, rows *Rows) ([]int, error) {
	r, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer r.Close()

	gr, err := gzip.NewReader(r)
	if err != nil {
		return nil, err
	}
	defer gr.Close()

	br := bufio.NewReader(gr)

	var buf bytes.Buffer
	var dims []int
	nameToDim := map[int]int{}

	frId := -1
	var toIds []int

	for {
		b, p, err := br.ReadLine()
		if err == io.EOF {
			if len(toIds) > 0 {
				rows.Add(frId, toIds)
			}
			return dims, nil
		} else if err != nil {
			return nil, err
		}

		buf.Write(b)
		if p {
			continue
		}

		line := buf.String()
		buf.Reset()

		if strings.HasPrefix(line, "#") {
			continue
		}

		ix := strings.Index(line, "\t")
		if ix < 0 {
			return nil, fmt.Errorf("invalid line: %s", line)
		}

		ln, err := strconv.ParseInt(line[:ix], 10, 64)
		if err != nil {
			return nil, err
		}

		rn, err := strconv.ParseInt(line[ix+1:], 10, 64)
		if err != nil {
			return nil, err
		}

		lid := DimFor(nameToDim, &dims, int(ln))
		rid := DimFor(nameToDim, &dims, int(rn))

		if lid == frId || frId < 0 {
			frId = lid
			toIds = append(toIds, rid)
			continue
		}

		rows.Add(frId, toIds)
		frId = lid
		toIds = toIds[:0]
		toIds = append(toIds, rid)
	}
}

func ComputeL1Norm(a, b []float64) float64 {
	s := 0.0
	for i, n := 0, len(a); i < n; i++ {
		s += math.Abs(a[i] - b[i])
	}
	return s
}

func Rank(rows *Rows, beta, epsilon float64) []float64 {
	n := len(rows.Rows)
	a := make([]float64, n)
	b := make([]float64, n)

	v := 1.0 / float64(n)
	for i := 0; i < n; i++ {
		a[i] = v
	}

	for {

		for i := 0; i < n; i++ {
			b[i] = 0.0
		}

		s := 0.0

		for i := 0; i < n; i++ {
			row := rows.Rows[i]
			for j, m := 0, len(row.Dims); j < m; j++ {
				b[i] += a[row.Dims[j]] * row.Vals[j] * beta
			}

			s += b[i]
		}

		z := (1.0 - s) / float64(n)
		for i := 0; i < n; i++ {
			b[i] += z
		}

		d := ComputeL1Norm(a, b)
		if d < epsilon {
			return b
		}

		a, b = b, a
	}
}

func main() {
	flag.Parse()

	if flag.NArg() != 1 {
		fmt.Fprintln(os.Stderr, "usage: pr file.gz")
		os.Exit(1)
	}

	var rows Rows
	dims, err := ReadMatrix(flag.Arg(0), &rows)
	if err != nil {
		log.Panic(err)
	}

	r := Rank(&rows, 0.8, 1e-10)

	for i, n := 0, len(r); i < n; i++ {
		fmt.Printf("% 6d: %0.3e\n", dims[i], r[i])
	}
}
