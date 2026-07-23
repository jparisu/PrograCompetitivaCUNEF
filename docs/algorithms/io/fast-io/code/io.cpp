// Fast I/O — put these two lines at the very start of main():
ios::sync_with_stdio(false);
cin.tie(nullptr);
// Then read/write as usual (now unbuffered from C stdio, much faster):
//   int x; cin >> x;          // input
//   cout << x << "\n";         // output ('\n' is faster than endl)
