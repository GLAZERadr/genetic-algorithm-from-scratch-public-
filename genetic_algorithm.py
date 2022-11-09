#mengimpor modul 
import random
import math
import numpy as np

#inisialisasi parameter banyak populasi dan panjang kromosom
tot_pop = 10
len_chromosom = 8

#1. init populasi 
#inisialisasi kromosom tipe data string dan mengggunakan operator assignment agar dalam perulangan variabel kromosom akan terus bertambah sebanyak panjang kromsom
#fungsi menerima 1 parameter yaitu panjang kromosom
def generate_kromosom(len_chromosom):

    kromosom = ""
    for i in range(len_chromosom):
        kromosom += str(random.randint(0, 9))

    return kromosom

#insisialisasi populasi dengan list kosong dan memanggil fungsi generate_kromosom untuk mengisi list tersebut
#fungsi menerima 2 parameter yaitu banyak populasi dan panjang kromosom
def generate_populasi(tot_pop, len_chromosom):

    populasi = []

    for i in range(tot_pop):
        populasi.append(generate_kromosom(len_chromosom))

    return populasi

#mengubah kromosom menjadi kromosom x dan y dengan membagi kromosom menjadi 2 bagian dan diubah menjadi bilangan desimal menggunakan rumus yang diberikan pada representasi integer
def decode(kromosom):

    kromosom_x = int(kromosom[:(len_chromosom//2)])
    kromosom_y = int(kromosom[(len_chromosom//2):])
    x = -5 + ((kromosom_x-0) /
              (int("9"*len(kromosom[:(len_chromosom//2)]))-0))*(5-(-5))
    y = -5 + ((kromosom_y-0) /
              (int("9"*len(kromosom[(len_chromosom//2):]))-0))*(5-(-5))

    return x, y

#2. kalkulasi fitness
#fungsi untuk menghitung fungsi heuristik yang diberikan
def heuristic(x, y):
    return (math.cos(x) + math.sin(y))**2 / (x**2 + y**2)

#menghitung fitness dengan metode minimize
#rumus : f = 1/(h + a), a digunakan agar fitness tidak bernilai 0
def fitness(kromosom):
    return 1/(heuristic(decode(kromosom)[0], decode(kromosom)[1])+ 0.000000001)

#3. seleksi menggunakan roulette wheel selection
#metode ini dilakukan dengan cara menghitung nilai fitness dari setiap kromosom dan kemudian dijumlahkan, lalu dibagi dengan jumlah total fitness sehingga menghasilkan nilai probabilitas, kemudian nilai probabilitas tersebut dijumlahkan dan dibagi dengan banyaknya populasi sehingga menghasilkan nilai probabilitas kumulatif, kemudian nilai probabilitas kumulatif tersebut dibandingkan dengan nilai random yang dihasilkan oleh fungsi random.random() dan jika nilai probabilitas kumulatif lebih besar dari nilai random maka kromosom tersebut akan dipilih
def roulette_wheel_selection(gen):
    total_fitness = sum([fitness(kromosom) for kromosom in gen])
    rel_fitness = [fitness(kromosom)/total_fitness for kromosom in gen]
    prob = [sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))]
    parent = []
    for _ in range(len(gen)):
        for (i, individual) in enumerate(gen):
            if random.random() <= prob[i]:
                parent.append(individual)
                break
    return parent

#4. crossover dengan metode multi point crossover
#metode ini dilakukan dengan cara memilih titik potong secara random dan kemudian menggabungkan kromosom dengan titik potong tersebut
#jika probabilitas crossover lebih besar dari nilai random yang dihasilkan oleh fungsi random.random() maka kromosom tersebut akan dipilih untuk dilakukan crossover
def multi_point_crossover(kromosom1, kromosom2):
    p_c = 0.9
    anak1 = kromosom1
    anak2 = kromosom2
    if random.random() < p_c:
        cross = random.randint(0, len(kromosom1) - 1)
        anak1 = kromosom1[:cross] + kromosom2[cross:]
        anak2 = kromosom2[:cross] + kromosom1[cross:]
    return anak1, anak2

#5. mutasi dengan metode mengganti 1 genotipe dengan angka random
#jika probabilitas mutasi lebih besar maka akan dilakukan mutasi dengan cara mengganti 1 genotipe dengan angka random
def mutasi(kromosom):
    p_m = 1/8
    for i in range(len(kromosom)):
        if random.random() < p_m:
            kromosom = kromosom[:i] + str(random.randint(0, 9)) + kromosom[i+1:]

    return kromosom

#6. metode penggantian generasi secara steady 
#steady state yaitu dengan cara mengganti generasi lama dengan generasi baru 
def next_generation(gen):
    selection = roulette_wheel_selection(gen)
    next_gen = []
    for i in range(0, len(gen), 2):
        anak1, anak2 = multi_point_crossover(selection[i], selection[i+1])
        next_gen.append(mutasi(anak1))
        next_gen.append(mutasi(anak2))
    result = []
    gen.sort(key=lambda x: fitness(x), reverse=True)
    result = next_gen

    return result

def print_generasi(generasi):
    for i in range(len(generasi)):
        print("\"{}\" ({:5f},{:5f}) : {}".format(generasi[i], decode(
            generasi[i])[0], decode(generasi[i])[1], fitness(generasi[i])))


#fungsi main untuk kalkulasi banyaknya generasi dan juga mengeluarkan output individu terbaik 
def main():
    generasi = []
    generasi = generate_populasi(tot_pop, len_chromosom)
    print("Generasi 1")
    print_generasi(generasi)
    best = generasi.sort(key=lambda x: fitness(x), reverse=True)
    best = generasi[0]

    #perulanagan komputasi GA sebanyak generasi yang diinginkan oleh user
    iterasi = 10
    for i in range(iterasi):
        generasi = next_generation(generasi)
        print("Generasi {}".format(i))
        print_generasi(generasi)

    print("-"*50)
    print("berhenti di generasi ke {}".format(i))
    print("kromosom terbaik : {}\t".format(best.split()), 
    "fitness terbaik  : {}\t".format(fitness(best)), 
    "nilai x          : {}\t".format(decode(best)[0]), 
    "nilai y          : {}\t".format(decode(best)[1]), sep = "\n")


if __name__ == "__main__":
    main()