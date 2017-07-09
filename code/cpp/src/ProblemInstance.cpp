#include "ProblemInstance.hpp"
#include "Utility.hpp"
#include <algorithm>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <sstream>
#include <string>

ProblemInstance::ProblemInstance(const int numTasks, const int numSubsets, const int numSubsetsToSelect)
: _numTasks(numTasks)
, _numSubsets(numSubsets)
, _numSubsetsToSelect(numSubsetsToSelect)
, _timeStampStr(util::getCurrentTimeStamp()) {
    if(_numTasks <= 0 || _numSubsets <= 0 || _numSubsetsToSelect <= 0)
        throw util::MSCPException("invalid data provided");

    // create a vector with task indices.
    std::vector<int> taskIndices(_numTasks);
    std::iota(taskIndices.begin(), taskIndices.end(), 0);

    // create a uniform random number generator.
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dis(0, _numTasks - 1);

    // generate subsets by:
    // - randomly permuting the vector,
    // - selecting a random number r in [0, _numTasks - 1],
    // - collecting element 0 to element r as the subset.
    for(int i = 0; i < _numSubsets; ++i) {
        std::shuffle(taskIndices.begin(), taskIndices.end(), gen);
        const int index = dis(gen);

        std::vector<int> currSubset(taskIndices.begin(), taskIndices.begin() + index + 1);
        std::sort(currSubset.begin(), currSubset.end());
        _subsets.emplace_back(std::move(currSubset));
    }
}

std::string ProblemInstance::getName() const {
    std::stringstream oss;
    oss << "instance_"
        << _numTasks << "_tasks_"
        << _numSubsets << "_subsets_"
        << _numSubsetsToSelect << "_to_select_"
        << _timeStampStr;

    return oss.str();
}

void ProblemInstance::writeToFile(const std::string& fileName) const {
    std::ofstream fout(fileName);

    fout << "Number of tasks (m): " << _numTasks << "\n";
    fout << "Number of subsets (n): " << _numSubsets << "\n";
    fout << "Number of subsets to select (k): " << _numSubsetsToSelect << "\n";

    fout << "Subsets:\n";
    for(const auto& currSubset : _subsets) {
        for(int index : currSubset)
            fout << " " << index;
        fout << "\n";
    }

    fout.close();
}

void ProblemInstance::print() const {
    std::cout << "Number of tasks (m): " << _numTasks << "\n";
    std::cout << "Number of subsets (n): " << _numSubsets << "\n";
    std::cout << "Number of subsets to select (k): " << _numSubsetsToSelect << "\n";

    std::cout << "subsets:\n";
    for(const auto& currSubset : _subsets) {
        for(int index : currSubset)
            std::cout << " " << index;
        std::cout << "\n";
    }
}
