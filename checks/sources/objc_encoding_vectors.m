// Owned finite compiler oracle; compiled to LLVM text, never linked or run.
struct Pair { int left; double right; };
union Choice { int integer; long long wide; };
struct Bits { unsigned int first:3; unsigned int second:5; };
const char *oracle_scalars = @encode(int);
const char *oracle_pointer = @encode(int **);
const char *oracle_const = @encode(const int *);
const char *oracle_array = @encode(int[3]);
const char *oracle_nested_array = @encode(int[2][3]);
const char *oracle_structure = @encode(struct Pair);
const char *oracle_union = @encode(union Choice);
const char *oracle_bitfields = @encode(struct Bits);
const char *oracle_object = @encode(id);
const char *oracle_selector = @encode(SEL);
const char *oracle_complex = @encode(double _Complex);
const char *oracle_atomic = @encode(_Atomic(int));
