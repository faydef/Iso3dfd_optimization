#coding:utf-8

import os 


def compile_all():
    Olevels = ["O1","O2","O3","Ofast"]
    Simds = ["sse","avx","avx2","avx512"]


    os.chdir("../iso3dfd-st7")
    if "compiled" not in os.listdir():
        print("creation du repertoire compiled...")
        os.system("rm bin/*")
        os.system("mkdir compiled")
        for olevel in Olevels :
            for simd in Simds: 
                os.system("make Olevel=-{} simd={} last".format(olevel,simd))
                os.system("mv bin/* compiled/bin_{}_{}.exe".format(olevel,simd))
    print("compilation of the code ...")

compile_all()
