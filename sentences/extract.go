package main

import (
	"archive/zip"
	"bufio"
	"bytes"
	"flag"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
)

var eol = []byte{'\n'}

func copy(r io.Reader, w io.Writer, n int) error {
	var buf bytes.Buffer
	br := bufio.NewReader(r)

	c := 0
	for {
		if c >= n {
			return nil
		}

		b, p, err := br.ReadLine()
		if err == io.EOF {
			return nil
		} else if err != nil {
			return err
		}

		buf.Write(b)
		if p {
			continue
		}

		if _, err := w.Write(buf.Bytes()); err != nil {
			return err
		}

		if _, err := w.Write(eol); err != nil {
			return err
		}

		buf.Reset()

		c++
	}
}

func copyLines(src, dst string, n int) error {
	zr, err := zip.OpenReader(src)
	if err != nil {
		return err
	}
	defer zr.Close()

	if len(zr.File) < 1 {
		return fmt.Errorf("no files found in archive: %s", src)
	}

	r, err := zr.File[0].Open()
	if err != nil {
		return err
	}
	defer r.Close()

	fw, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer fw.Close()

	zw := zip.NewWriter(fw)
	defer zw.Close()

	// Remove the extension, which should be zip
	name := dst[:len(dst)-len(filepath.Ext(dst))]

	w, err := zw.Create(name)
	if err != nil {
		return err
	}

	return copy(r, w, n)
}

func main() {
	flagN := flag.Int("n", 50000, "")
	flagSrc := flag.String("src", "sentences.txt.zip", "source file")
	flagDst := flag.String("dst", "test.txt.zip", "destination file")
	flag.Parse()

	if err := copyLines(*flagSrc, *flagDst, *flagN); err != nil {
		log.Panic(err)
	}
}
