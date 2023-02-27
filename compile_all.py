#coding:utf-8

import os 


def compile_all():
    Olevels = ["01","02","03","0fast"]
    Simds = ["sse","avx","avx2","avx512"]


    os.chdir("../iso3dfd-st7")
    print(os.listdir())
    if "compiled" not in os.listdir():
        print("creation du repertoire compiled...")
        os.system("rm bin/*")
        os.system("mkdir compiled")
        for olevel in Olevels :
            for simd in Simds: 
                os.system("make Olevel=-{} simd={} last".format(olevel,simd))
                os.system("mv bin/* compiled/bin_{}_{}.exe".format(olevel,simd))

#compile_all()
