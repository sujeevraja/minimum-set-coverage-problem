#ifndef SOLVER_HPP
#define SOLVER_HPP

#include <string>
#include <vector>
#include <boost/optional.hpp>

#ifdef USE_CBC
class CoinModel;
#endif

struct ColumnInfo {
     ColumnInfo(int i, boost::optional<double> l, boost::optional<double> u, double o, const std::string * namePtr)
     : index(i)
     , lb(l)
     , ub(u)
     , obj(o)
     , name(namePtr != nullptr ? *namePtr : "") {}

     int index;
     boost::optional<int> lb;
     boost::optional<int> ub;
     double obj;
     std::string name;
 };

class Solver {
public:
    Solver();
    ~Solver();

    void addColumn(const int index, const boost::optional<double> lb, const boost::optional<double> ub,
        const double obj, const std::string * name = nullptr);

    void markColAsInteger(const int index);

    void addRow(const std::vector<int>& indices, const std::vector<double>& coefs,
        const boost::optional<double> lb, const boost::optional<double> ub);

    void printModelData() const;

#ifdef USE_CBC
    void prepareModelForCbc();

    void writeMpsFile(const std::string& fileName) const;

    void solveWithCbc();
#endif

    const std::vector<double>& getSolution() const {
        return _solution;
    }

private:

    int _numCols;
    std::vector<ColumnInfo> _columns;
    std::vector<int> _integerColIndices;
    std::vector<std::vector<int>> _rowIndices;
    std::vector<std::vector<double>> _rowCoefs;
    std::vector<std::pair<boost::optional<double>, boost::optional<double>>> _rowBounds;
    std::vector<double> _solution;

#ifdef USE_CBC
    // Using raw pointers as it is recommended not to use C++11 smart pointers with COIN-OR classes.
    CoinModel * _build;
#endif
};

#endif
