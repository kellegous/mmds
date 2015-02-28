
#include <memory>
#include <stdio.h>
#include <unistd.h>
#include <sys/fcntl.h>
#include <string>
#include <unordered_map>
#include <math.h>
#include <zlib.h>

#include "status.h"
#include "util.h"

namespace {

typedef std::unordered_map<int, int> IdMap;

class Row {
 public:
  std::vector<double> vals;
  std::vector<int> dims;
 private:
};

class Rows {
 public:
  Rows() {
    rows_.reserve(500000);
  }

  ~Rows() {
    for (int i = 0, n = rows_.size(); i < n; i++) {
      delete rows_[i];
    }
  }

  Row* get(int i) {
    return rows_[i];
  }

  size_t Size() {
    return rows_.size();
  }

  void Add(int frid, std::vector<int>& toid) {
    double f = 1.0 / (double)toid.size();
    ReserveFor(frid);
    for (int i = 0, n = toid.size(); i < n; i++) {
      ReserveFor(toid[i]);
      Row* r = rows_[toid[i]];
      r->vals.push_back(f);
      r->dims.push_back(frid);
    }
  }
 private:
  void ReserveFor(int id) {
    if (id < rows_.size()) {
      return;
    }
    // rows_.reserve(id + 1);
    while (id >= rows_.size()) {
      rows_.push_back(new Row);
    }
  }

  std::vector<Row*> rows_;
};


int DimFor(IdMap* name_to_dim, std::vector<int>* dims, int name) {

  std::pair<IdMap::iterator, bool> r = name_to_dim->insert(
    IdMap::value_type(name, dims->size()));
  if (r.second) {
    dims->push_back(name);
  }

  return r.first->second;
}

Status ReadGraph(const char* filename, Rows* rows, std::vector<int>* dims) {

  IdMap name_to_dim;

  gzFile fd = gzopen(filename, "rb");
  if (fd == 0) {
    return ERR("unable to open file");
  }

  std::string line;

  int frId = -1;
  std::vector<int> toIds;

  static const size_t BUFFER_SIZE = 16*1024;
  char buf[BUFFER_SIZE + 1];
  while (size_t n = gzread(fd, buf, BUFFER_SIZE)) {
    if (n == (size_t)-1) {
      return ERR("read error");
    }

    if (!n) {
      break;
    }

    char* p = buf;
    for (;;) {
      char* c = (char*)memchr(p, '\n', (buf + n) - p);
      if (c == NULL) {
        line.assign(p, (buf + n) - p);
        break;
      }

      line.append(p, (size_t)(c - p));
      p = c + 1;

      if (line[0] == '#') {
        line.clear();
        continue;
      }

      size_t ix = line.find('\t');
      if (ix == std::string::npos) {
        return ERR("invalid line");
      }

      int ln, rn;

      std::string lns(line.substr(0, ix));
      Status did = util::ParseInt(lns, 10, &ln);
      if (!did.ok()) {
        return did;
      }

      // take the stupid \r off the end.
      int e = line.size() - 1;
      while (line[e] == '\r') {
        e--;
      }

      std::string rns(line.substr(ix + 1, e-ix));
      did = util::ParseInt(rns, 10, &rn);
      if (!did.ok()) {
        return did;
      }

      line.clear();
      ln = DimFor(&name_to_dim, dims, ln);
      rn = DimFor(&name_to_dim, dims, rn);

      if (ln == frId || frId < 0) {
        frId = ln;
        toIds.push_back(rn);
        continue;
      }

      rows->Add(frId, toIds);
      frId = ln;
      toIds.clear();
      toIds.push_back(rn);
    }
  }

  if (!toIds.empty()) {
    rows->Add(frId, toIds);
  }

  gzclose(fd);
  return NoErr();
}

double ComputeL1Norm(double* a, double* b, size_t n) {
  double s = 0.0;
  for (int i = 0; i < n; i++) {
    s += fabs(a[i] - b[i]);
  }
  return s;
}

double* Rank(Rows& rows, double beta, double epsilon) {
  size_t n = rows.Size();
  double* a = new double[n];
  double* b = new double[n];

  double v = 1.0 / (double)n;
  for (int i = 0; i < n; i++) {
    a[i] = v;
  }

  for (;;) {
    memset(b, 0, sizeof(double)*n);

    double s = 0.0;

    for (int i = 0; i < n; i++) {
      Row* row = rows.get(i);
      for (int j = 0, m = row->dims.size(); j < m; j++) {
        b[i] += a[row->dims[j]] * row->vals[j] * beta;
      }
      s += b[i];
    }

    s = (1.0 - s) / (double)n;
    for (int i = 0; i < n; i++) {
      b[i] += s;
    }

    double d = ComputeL1Norm(a, b, n);
    if (d < epsilon) {
      delete[] a;
      return b;
    }

    double* t = a;
    a = b;
    b = t;
  }
}

} // anonymous

int main(int argc, char* argv[]) {
  Rows rows;
  std::vector<int> dims;

  if (argc < 2) {
    fprintf(stderr, "usage: %s file.gz\n", argv[0]);
    return 1;
  }

  Status did = ReadGraph(argv[1], &rows, &dims);
  if (!did.ok()) {
    fprintf(stderr, "ERROR %s\n", did.what());
    return 1;
  }

  double* r = Rank(rows, 0.8, 1e-10);

  for (int i = 0, n = dims.size(); i < n; i++) {
    printf("%*d: %0.3e\n", 6, dims[i], r[i]);
  }

  return 0;
}