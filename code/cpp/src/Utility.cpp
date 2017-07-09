#include "Utility.hpp"
#include <chrono>
#include <ctime>
#include <sys/types.h>
#include <sys/stat.h>

std::string util::getCurrentTimeStamp() {
    auto endChrono = std::chrono::system_clock::now();
    std::time_t endTime = std::chrono::system_clock::to_time_t(endChrono);

    std::string timeStr(std::ctime(&endTime));
    std::replace_if(timeStr.begin(), timeStr.end(), [](const char c) {
        return c == ' ' || c == ':';
    }, '_');

    timeStr.erase(timeStr.begin(), timeStr.begin() + 4);
    timeStr.erase(std::prev(timeStr.end()));
    return timeStr;
}

bool util::folderExists(const std::string& dirName) {
   struct stat info;
   return stat(dirName.c_str(), &info) == 0;
}
