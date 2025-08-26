#!/bin/bash
set -e

echo "🚀 Building jank in Ubuntu proot environment"

# Copy jank source to Ubuntu
echo "📦 Copying jank source to Ubuntu..."
proot-distro login ubuntu -- mkdir -p /root/jank
proot-distro login ubuntu -- rm -rf /root/jank/*

# Use rsync-style copy
cp -r jank/* ~/.tmp_jank_copy/ 2>/dev/null || true
mkdir -p ~/.tmp_jank_copy 2>/dev/null || true
rsync -av jank/ ~/.tmp_jank_copy/ 2>/dev/null || cp -r jank/* ~/.tmp_jank_copy/

echo "🔧 Installing dependencies in Ubuntu..."
proot-distro login ubuntu -- bash -c "
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -yqq wget curl gnupg lsb-release
    
    # Install LLVM 21
    wget -qO- https://apt.llvm.org/llvm-snapshot.gpg.key | tee /etc/apt/trusted.gpg.d/apt.llvm.org.asc
    echo 'deb http://apt.llvm.org/noble/ llvm-toolchain-noble-21 main' > /etc/apt/sources.list.d/llvm.list
    apt-get update -qq
    apt-get install -yqq llvm-21-dev clang-21 lld-21 cmake ninja-build git build-essential
    
    # Set up alternatives for LLVM/Clang
    update-alternatives --install /usr/bin/llvm-config llvm-config /usr/bin/llvm-config-21 100
    update-alternatives --install /usr/bin/clang clang /usr/bin/clang-21 100
    update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-21 100
"

echo "🏗️ Building jank..."
proot-distro login ubuntu -- bash -c "
    cd /root
    rm -rf jank
    git clone --recursive https://github.com/jank-lang/jank || exit 1
    cd jank
    
    # Configure with LLVM 21
    cmake -S compiler+runtime -B build -G Ninja -DCMAKE_BUILD_TYPE=Release \\
        -DLLVM_DIR=\$(llvm-config-21 --cmakedir) \\
        -DCMAKE_C_COMPILER=clang-21 \\
        -DCMAKE_CXX_COMPILER=clang++-21 || exit 1
    
    # Build (with limited parallelism for mobile)
    cmake --build build -j2 || exit 1
    
    echo '✅ jank build complete!'
    ls -la build/
"

echo "🎉 jank is ready in Ubuntu proot at /root/jank/build/"