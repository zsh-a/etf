#include<iostream>
#include <type_traits>
#include <vector>
using namespace std;


#include <iostream>
#include<vector>
template<typename _Tp>
  _GLIBCXX_NODISCARD
  constexpr _Tp&&
  forward2(typename std::remove_reference<_Tp>::type& __t) noexcept
  { 
    std::cout << "1\n";
    // static_assert(std::is_same_v<_Tp,std::vector<int>&>);
    return static_cast<_Tp&&>(__t);
   }

/**
  *  @brief  Forward an rvalue.
  *  @return The parameter cast to the specified type.
  *
  *  This function is used to implement "perfect forwarding".
  */
// template<typename _Tp>
//   _GLIBCXX_NODISCARD
//   constexpr _Tp&&
//   forward2(typename std::remove_reference<_Tp>::type&& __t) noexcept
//   {
//     std::cout << "2\n";
//     static_assert(!std::is_lvalue_reference<_Tp>::value,
//   "std::forward must not be used to convert an rvalue to an lvalue");
//     return static_cast<_Tp&&>(__t);
//   }
void foo(std::vector<int>& x) {
    std::cout << "lvalue: " << std::endl;
}

void foo(std::vector<int>&& x) {
    std::cout << "rvalue: "  << std::endl;
}

template<typename T>
void bar(T&& x) {
  static_assert(std::is_same_v<decltype(x),std::vector<int>&&>);
  foo(forward2<T>(x));
}

int main()
{
  std::vector<int> i = {1,2,3};
  // bar(i); // 调用左值引用版本
  bar(std::move(i)); // 调用左值引用版本
}