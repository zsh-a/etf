#include <mutex>

using namespace std;

mutex mu;
int main(){

    std::unique_lock<mutex> lock(mu);
    std::unique_lock<mutex> lock2(mu);
}