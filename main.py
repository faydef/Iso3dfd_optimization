#!coding:utf-8

type_algo = int(input("Which algorithm would you want to execute ? classic ant colony (0) or tree ant colony (1) ? "))
while type_algo not in [0,1]:
    print("please enter a valid algorithm")
if type_algo == 0 :
    print("execution of classic ant colony...")
    ###
if type_algo == 1: 
    print("exection of ant colony on a tree...") 
    ###
