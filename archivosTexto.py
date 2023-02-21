'''
f=open('alumnos.txt','r')

#Leer el contenido del archivo
#nombre= f.read()
#print(nombre)


nombres2= f.readlines()
print(nombres2)

f.close()

for items in nombres2:
    print(items, end='')

'''

alumno={'Matricula':12345, 'Nombre': 'Mario', 'Apellidos':'Lopez', 'Correo':'sergioqlbq@gmail.com'}
f=open('alumnos.txt','a')
for clave, valor in alumno.items():
        f.write('\n'+clave + ':' + str(valor))    
       
f.close()





