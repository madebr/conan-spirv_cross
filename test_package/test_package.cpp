#include <spirv_cross/spirv_cross.hpp>

int main()
{
    SPIRV_CROSS_NAMESPACE::Compiler compiler({
        0x07230203, // magic number
        0x00010000, // version 1.0.0
        0x00080001, // Khronos Glslang Reference Front End;
        63,         // Bound: 63
        0});        // Schema: 0
    compiler.compile();
    return 0;
}
