class Pasta:
    def __init__(self, nome, arquivos, pastas, pai=None):
        self.nome = nome
        self.pai = pai
        self.arquivos = arquivos
        self.pastas = pastas  
    
class Arquivo:
    def __init__(self, nome, conteudo=""):
        self.nome = nome
        self.conteudo = conteudo
        
def autores():
    print("\033[95m" + "A L A N A   C A R O L I N A" + "\033[0m")
    print("\033[96m" + "M A T E U S   O L I V E I R A" + "\033[0m")
    print("\033[38;5;208m" + "R A F A E L   A R G Ô L O" + "\033[0m")
    print("\n\n:DD")

# Comando mkdir
def mkdir(dir_atual, comandos):
    
    caracteresEspecias = ['\\', '/', ' ', ':', '*', '?', '"', '<', '>', '|']
    
    for letra in comandos[1]: 
        if (letra in caracteresEspecias):
            print("bash: mkdir: " + comandos[1] + ": Invalid argument")
            return
        
    for pasta in dir_atual.pastas:
        if pasta.nome == comandos[1]:
            print("bash: mkdir: cannot create directory '" + comandos[1] + "': File exists")
            return
    
    novaPasta = Pasta(comandos[1], [], [], dir_atual)
    dir_atual.pastas.append(novaPasta)
    
# Caminho absoluto
def caminho_absoluto(dir_atual, path, comandos, string="", mudar=True, copia=""):
       
    if (mudar): # /home/c ["", "c"]
        copia = comandos
        
    encontrado = False
    
    if (dir_atual.nome == "/"): # /
        string += dir_atual.nome 
    else: 
        string += dir_atual.nome + "/"
        
    print("string: ", string)
        
        
    for pasta in dir_atual.pastas:
        
        if (pasta.nome == comandos[1]):
            
            encontrado = True
            
            dir_atual = pasta # ["", "a", "b"]
            
            comandos.pop(1) # ["", "b"]
            
            existe = verificar(dir_atual, comandos)
                           
            if (existe):  
                if (len(comandos) == 2):
                    
                    for pasta in dir_atual.pastas:
                        if (pasta.nome == comandos[1]):
                            string += dir_atual.nome + "/"
                            dir_atual = pasta
                            
                    string += dir_atual.nome
                    
                    path = "\033[1m\033[38;2;44;199;119mpc1@pc1-pc1\033[0m\033[0m:\033[1m\033[38;2;43;99;240m" + string + "\033[0m\033[0m"
                    
                    break
                
                mudar = False
                return caminho_absoluto(dir_atual, path, comandos, string, mudar, copia)
            else:
                print("Vetor no else: ", copia)
                string1 = "bash: cd:"
                string2 = ": No such file or directory"
                
                dirs = ""
                for dir in copia:
                    dirs += dir + "/"
                
                print(string1, dirs, string2)
                
                return
            
    if (not encontrado):
        
        string1 = "bash: cd:"
        string2 = ": No such file or directory"
        
        dirs = ""
        for dir in copia:
            if (dir != ""):
                dirs += "/" + dir + ''
        
        print(string1, dirs, string2)
        return
    
    return dir_atual, path
               
# Comando cd para voltar mais de um diretório
def cdDiretorios(dir_atual, path, qtd, root):
        
    for i in range(qtd, 0, -1):  
              
        if (dir_atual.nome == "/" and i != 1):
            path += "/\033[0m"
            return root, path
        
        dir_atual = dir_atual.pai
        
        index_barra = path.rfind('/')
        if (index_barra != -1):
            path = path[:index_barra]
            
    
    path += "/\033[0m"
    
    return dir_atual, path
                  
# Comando cd
def cd(path, dir_atual, comandos, root): 
    
    if (comandos[1] == "/" and len(comandos[1]) == 1):
        dir_atual = root
        path = "\033[1m\033[38;2;44;199;119mpc1@pc1-pc1\033[0m\033[0m:\033[1m\033[38;2;43;99;240m/\033[0m\033[0m"
        return dir_atual, path
    
    if (comandos[1][0] == "/"): # cd /usr/c
        dir_atual = root
        
        f = comandos[1] # /usr
        folder = f.split("/") # ["", "usr", "c"]
        
        if (len(folder) == 2):
            
            for pasta in root.pastas:
                if pasta.nome == folder[1]:
                    dir_atual = pasta
                    path = "\033[1m\033[38;2;44;199;119mpc1@pc1-pc1\033[0m\033[0m:\033[1m\033[38;2;43;99;240m/" + folder[1] + "\033[0m\033[0m"
                    return dir_atual, path
        
        if (len(folder[1]) > 2):
            
            try:
                dir_atual, path = caminho_absoluto(dir_atual, path, folder)
            except:
                return dir_atual, path
            
            return dir_atual, path
        
        try:
            dir_atual_copia = root 
            path_copia = path
            dir_atual_copia, path_copia = caminho_absoluto(dir_atual_copia, path_copia, folder, root)
            
            
            return dir_atual_copia, path_copia
        except:
            pass
        
        return dir_atual, path
    
    # Verifica 
    cont = 0
    qtd = 0
    for letra in comandos[1]: # cd ../.. 
        if ("." in letra):
            cont += 1
            
    if (cont > 2): 
        if (cont % 2 == 0):
            qtd = int(cont / 2)
            dir_atual, path = cdDiretorios(dir_atual, path, qtd, root)
            return dir_atual, path
        else:
            print("bash: cd: " + comandos[1] + ": Invalid argument")
        
    
    if ('/' in comandos[1]):
        dir_atual, path = caminho_relativo(dir_atual, comandos, path)
        return dir_atual, path
    
    pasta_encontrada = True
    
    # Se for para entrar numa pasta
    if (comandos[1] != ".."): # cd home
        pasta_encontrada = verificar(dir_atual, comandos)
        
    # Se for para voltar uma pasta
    elif (comandos[1] == ".."):
        if (dir_atual.nome == "/"):
            return dir_atual, path
        for i in range(len(path) - 1, -1, -1):
            if (path[i] == "/"):
                if (dir_atual.pai.nome == "/"): # [a, b, c, d]
                    path = path[:i + 1] + "\033[0m\033[0m"
                else:
                    path = path[:i] + "\033[0m" 
                    
                dir_atual = dir_atual.pai
                return dir_atual, path
    
    if (not pasta_encontrada):
        print("bash: cd: /" + comandos[1] + ": No such file or directory")
        return dir_atual, path
    
    # Se a pasta existir, atualiza o caminho e o diretorio
    for pasta in dir_atual.pastas: # cd home
        if (pasta.nome == comandos[1]):
            
            # Se a pasta anterior for a raiz
            if (pasta.pai.nome ==  "/"):
                path += "\033[1m\033[38;2;43;99;240m" + comandos[1] + "\033[0m\033[0m"
                
            # Se a pasta anterior não for a raiz
            else: 
                
                path += "\033[1m\033[38;2;43;99;240m/" + comandos[1] + "\033[0m\033[0m"
            
            for pasta in dir_atual.pastas:
                if (comandos[1] == pasta.nome):
                    dir_atual = pasta 
                    return dir_atual, path         
            break
                 
    try:
        return dir_atual, path
    except:
        return 

# Comando find
def find(root, comandos, caminho=""): 
               
    for arquivo in root.arquivos:
        if (comandos[1] in arquivo.nome):
            pwd(root, "true")
            print("/"+ str(arquivo.nome))
        
    for pasta in root.pastas:      
                
        if (comandos[1] in pasta.nome):
            pwd(pasta, "")     
        
        if (len(pasta.pastas) > 0 or len(pasta.arquivos) > 0):
            find(pasta, comandos, caminho)
                
# Comando ls
def ls(dir_atual):
    for pasta in dir_atual.pastas:
        print("  " + "\033[1m\033[38;2;43;99;240m" + pasta.nome + "\033[0m\033[0m", end="")
        
    for arquivo in dir_atual.arquivos:
        print("  " + "\033[1m" + arquivo.nome + "\033[0m", end="")
        
    if (len(dir_atual.arquivos) > 0 or len(dir_atual.pastas) > 0):
        print("")

# Comando touch
def touch(dir_atual, comandos):
    novoArquivo = Arquivo(comandos[1])
    dir_atual.arquivos.append(novoArquivo)

# Comando rm
def rm(dir_atual, comandos):
    
    arquivo_encontrado = verificar(dir_atual, comandos)
    
    if (not arquivo_encontrado):
        print("bash: rm: " + comandos[1] + ": No such file or directory")
        return dir_atual
    
    # Loop para pastas
    for pasta in dir_atual.pastas:
        if (pasta.nome == comandos[1]):
            if (len(pasta.arquivos) > 0 or len(pasta.pastas) > 0):
                print("bash: rm: " + comandos[1] + ": Is a directory")
                return dir_atual
            dir_atual.pastas.remove(pasta)
            break
    
    # Loop para arquivos
    for arquivo in dir_atual.arquivos:
        if (arquivo.nome == comandos[1]):
            arquivo_encontrado = True
            dir_atual.arquivos.remove(arquivo)
            break
        
    return dir_atual

# Comando nano
def nano(dir_atual, comandos):
    
    arquivo_encontrado = verificar(dir_atual, comandos)
    
    if (not arquivo_encontrado):
        print("bash: nano: " + comandos[1] + ": No such file or directory")
        return dir_atual
    
    for arquivo in dir_atual.arquivos:
        if (arquivo.nome == comandos[1]):
            conteudo = input()
            arquivo.conteudo = conteudo 
            break
    
    return dir_atual

# Comando mv
def mv(dir_atual, path, comandos, root):
    
    if ("/" in comandos[2]): # mv a ../../../b
        cont = 0
        qtd = 0
        for letra in comandos[2]:
            if ("." in letra):
                cont += 1 
        
        if (cont > 2): 
            if (cont % 2 == 0):
                qtd = int(cont / 2)
                dir_atual = mv_diretorio(dir_atual, comandos, path, qtd, root)
                return dir_atual, path
            else:
                print("bash: cd: " + comandos[1] + ": Invalid argument")
            
    
    chave = False 
    
    if (comandos[2] == '.'):
        return dir_atual
    
    if (".."in comandos[2]):
        pass
            
    # Loop para arquivos
    arquivo_encontrado = False
    for arquivo in dir_atual.arquivos:
        if (arquivo.nome == comandos[1]):
            arquivo_encontrado = True
            arquivo.nome = comandos[2]
            chave = True
            break
        
    # Loop para pastas
    pasta_encontrada = False
    for pasta in dir_atual.pastas:
        if (pasta.nome == comandos[1]):
            pasta_encontrada = True
            pasta.nome = comandos[2]
            chave = True
            break
            
    if (not chave):
        if (not pasta_encontrada):
            print("bash: mv: " + comandos[1] + ": No such file or directory")
            
        else:
            if (not arquivo_encontrado):
                print("bash: mv: " + comandos[1] + ": No such file or directory")
                
    return dir_atual

def mv_diretorio(dir_atual, comandos, path, qtd, root):
    
    existe = verificar(dir_atual, comandos) # mv ../../b
    
    if (existe):
        for p1 in dir_atual.pastas:
            if (p1.nome == comandos[1]):
                path_copia = path
                dir_atual_copia = dir_atual
                dir_atual_copia, path_copia = cdDiretorios(dir_atual_copia, path_copia, qtd, root)
                dir_atual_copia.pastas.append(p1)
                dir_atual.pastas.remove(p1)
                
                return dir_atual
                        
                
    pass

# Comando cat
def cat(dir_atual, comandos):
    nao_encontrado = False
    for arquivo in dir_atual.arquivos:
        if (arquivo.nome == comandos[1]):
            print(arquivo.conteudo) 
            return 
            
    if (not nao_encontrado):
        print("bash: cat: " + comandos[1] + ": No such file or directory")

# Comando clear
def clear():
    print("\033c", end="")
    
# Comando pwd
def pwd(dir_atual, opcional):

    if (dir_atual.nome == "/" and opcional==""):
        print("/")
        return
    
    if (dir_atual.nome != "/"):
    
        caminho = ""
        while dir_atual:  
            caminho = "/" + dir_atual.nome + caminho 
            
            dir_atual = dir_atual.pai
            if (not dir_atual.pai):
                break
            
        if (opcional == "true"):
            print(caminho, end="")
        else:
            print(caminho)  

# Verificar arquivo/pasta existente
def verificar(dir_atual, comandos):
    
    elemento_encontrado = False
    
    for pasta in dir_atual.pastas:
        if (pasta.nome == comandos[1]):               
            dir_atual = pasta
            elemento_encontrado = True
            break
        
    for arquivo in dir_atual.arquivos:
        if (arquivo.nome == comandos[1]):
            dir_atual = arquivo
            elemento_encontrado = True
            break

    return elemento_encontrado

def quebrarDiretorio(dir_atual, comandos, path, string_caminho="", existe_dir=True): 
    
    print("Vetor: " , comandos)
    if (existe_dir and len(comandos) != 1): 
        for pasta in dir_atual.pastas:
            if (pasta.nome == comandos[1]):
                
                string_caminho += dir_atual.nome + "/"
                dir_atual = pasta
                
                if (dir_atual.pai.nome == "/"):
                    path += "\033[38;2;43;99;240m\033[1m" + dir_atual.nome + "\033[0m\033[0m"
                else:
                    path += "\033[38;2;43;99;240m\033[1m/" + dir_atual.nome + "\033[0m\033[0m"
                    
                comandos.pop(1)
                
                if (len(comandos) == 1):
                    return dir_atual, path
                
                break
            
        existe_dir = verificar(dir_atual, comandos)
        
        if (existe_dir):
            return quebrarDiretorio(dir_atual, comandos, path, string_caminho, existe_dir)

    string1 = "bash: cd:"
    string2 = ": No such file or directory"
    
    dirs = ""
    for dir in comandos:
        if (dir != ""):
            dirs += "/" + dir
    
    print(string1, dirs, string2)
        
    return     

def caminho_relativo(dir_atual, comandos, path):
    path_copia = path
    dir_atual_copia = dir_atual
    
    c = comandos[1]
    comandos = c.split("/") # ["", "a", "b", "c"]
    comandos.insert(0, "")
    
    try:
        dir_atual_copia, path_copia = quebrarDiretorio(dir_atual_copia, comandos, path_copia)
    except:
        pass
        
    return dir_atual, path