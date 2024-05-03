from funcoes import *

s = "$ "
path = "\033[1m\033[38;2;44;199;119mpc1@pc1-pc1\033[0m\033[0m:\033[1m\033[38;2;43;99;240m/\033[0m\033[0m"

root = Pasta("/", [], [], None)
dir_atual = root
root.pastas.append(Pasta("home", [], [], dir_atual))
root.pastas.append(Pasta("etc", [], [], dir_atual))
root.pastas.append(Pasta("bin", [], [], dir_atual))
root.pastas.append(Pasta("usr", [], [], dir_atual))
root.pastas.append(Pasta("sbin", [], [], dir_atual))
root.pastas.append(Pasta("lib", [], [], dir_atual))
root.pastas.append(Pasta("tmp", [], [], dir_atual))
root.pastas.append(Pasta("dev", [], [], dir_atual))
root.pastas.append(Pasta("root", [], [], dir_atual))
root.pastas.append(Pasta("proc", [], [], dir_atual))
root.pastas.append(Pasta("mnt", [], [], dir_atual))
root.pastas.append(Pasta("opt", [], [], dir_atual))
root.pastas.append(Pasta("var", [], [], dir_atual))

cmds = [
    "cd", "ls", "mkdir",
    "rm", "mv", "touch",
    "cat", "nano", "exit", 
    "pwd", "clear", "find", 
    "help", "autores"
]

print("'help' para ver comandos")

while (True):

    c = input(path + s)
    comandos = c.split()
    if (len(comandos) == 0):
        pass
    else:
        if (comandos[0] in cmds):
            if (len(comandos) < 3):
                
                # Comando cd
                if (comandos[0] == "cd"):            
                    dir_atual, path = cd(path, dir_atual, comandos, root)

                # Comando ls
                if (comandos[0] == "ls"):
                    ls(dir_atual)
                        
                # Comando mkdir
                if (comandos[0] == "mkdir"):
                    mkdir(dir_atual, comandos)
                
                # Comando touch
                if (comandos[0] == "touch"):
                    touch(dir_atual, comandos)
                    
                # Comando rm
                if (comandos[0] == "rm"):
                    dir_atual = rm(dir_atual, comandos)
                        
                # Comando cat
                if (comandos[0] == "cat"):
                    cat(dir_atual, comandos)      
                            
                # Comando mv
                if (comandos[0] == "mv"):
                    mv(dir_atual, comandos, root)
                    
                # Comando nano
                if (comandos[0] == "nano"):
                    dir_atual = nano(dir_atual, comandos)   
                    
                # Coamando pwd
                if (comandos[0] == "pwd"):
                    pwd(dir_atual, "")
                    
                # Comando clear
                if (comandos[0] == "clear"):
                    clear()
                
                # Comando exit
                if (comandos[0] == "exit"):
                    break
                
                # Comando find
                if (comandos[0] == "find"):
                    find(root, comandos)
                
                if (comandos[0] == "help"):
                    for cmd in cmds:
                        if (cmd != "help"):
                            print(cmd)
                            
                if (comandos[0] == "autores"):
                    autores()
            
            else:
                if (comandos[0] == "mv"):
                    mv(dir_atual, path, comandos, root)
        else:
            if (comandos[0] == ""):
                pass
            elif (len(comandos) > 0):
                print(f"{comandos[0]}: command not found")
            