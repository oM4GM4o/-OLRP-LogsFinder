from datetime import datetime
import glob
import os
import re

now = datetime.now()

PATHLOGS = "logs/"
PATHOUT = "output/"

txtfiles = []

def getDamage(fichiers, player, printmode):
    damage = []
    damagecount = 0;
    player.replace('.','[.]*')
    stringt = '((' + player + ').* has taken)|(has taken .*('+ player + '))|((' + player + ').* has dealt)|(has dealt .*('+ player + '))';
    searchstring = re.compile(stringt);
    for filename in fichiers:
        with open(filename, encoding="utf8") as file:
            for line in file:
                if searchstring.search(line):
                    damagecount += 1;
                    line = line.strip();
                    damage.append(re.sub('.log', '', re.sub('logs\\\\', '', filename)) + ' | '+ line);
    if printmode == 0:
        printLines(damage);
        print('|--------------------------------------------------------------------------\n' +
            player + ' a touché / a été touché ' + str(damagecount) + ' fois dans les fichiers log')
    elif printmode == 1:
        printFile(damage, player, 'damage');
    return damagecount;

def getMessages(fichiers, player, printmode):
    messages = []
    messagecount = 0;
    player.replace('.','[.]*')
    stringt = '('+ player + '.*/PM)|(OOC.*' + player + ')|('+ player + '.*says)|('+ player + '.*/A )';
    searchstring = re.compile(stringt);
    for filename in fichiers:
        with open(filename, encoding="utf8") as file:
            for line in file:
                if searchstring.search(line):
                    messagecount += 1;
                    line = line.strip();
                    messages.append(re.sub('.log', '', re.sub('logs\\\\', '', filename)) + ' | '+ line);
    if printmode == 0:
        printLines(messages);
        print('|--------------------------------------------------------------------------\n' +
            player + ' a envoyé ' + str(messagecount) + ' messages dans les fichiers log')
    elif printmode == 1:
        printFile(messages, player, 'messages');
    return messagecount;


def getKills(fichiers, player, printmode):
    kill = []
    killcount = 0;
    player.replace('.','[.]*')
    stringt = player + ' has dealt .*, killing them!';
    searchstring = re.compile(stringt);
    for filename in fichiers:
        with open(filename, encoding="utf8") as file:
            for line in file:
                if searchstring.search(line):
                    killcount += 1;
                    line = line.strip();
                    kill.append(re.sub('.log', '', re.sub('logs\\\\', '', filename)) + ' | '+ line);
    if printmode == 0:
        printLines(kill);
        print('|--------------------------------------------------------------------------\n' +
            player + ' a tué ' + str(killcount) + ' fois dans les fichiers log')
    elif printmode == 1:
        printFile(kill, player, 'kill');
    return killcount;

def getActivity(fichiers, player, printmode):
    activity = []
    for filename in fichiers:
        with open(filename, encoding="utf8") as file:
            for line in file:
                if line.find(player) != -1:
                    line = line.strip();
                    activity.append(re.sub('.log', '', re.sub('logs\\\\', '', filename)) + ' | '+ line);
    if printmode == 0:
        printLines(activity);
    elif printmode == 1:
        printFile(activity, player, 'activite');

def getMorts(fichiers, player, printmode):
    death = []
    deathcount = 0;
    player.replace('.','[.]*')
    stringt = 'to ' + player + '.*, killing them!';
    searchstring = re.compile(stringt);
    for filename in fichiers:
        with open(filename, encoding="utf8") as file:
            for line in file:
                if searchstring.search(line):
                    deathcount += 1;
                    line = line.strip();
                    death.append(re.sub('.log', '', re.sub('logs\\\\', '', filename)) + ' | '+ line);
    if printmode == 0:
        printLines(death);
        print('|--------------------------------------------------------------------------\n' +
            player + ' est mort ' + str(deathcount) + ' fois dans les fichiers logs')
    elif printmode == 1:
        printFile(death, player, 'morts');
    return deathcount;

def printFile(liste, value, name):
    fname = PATHOUT + name + "_" + str(value) + "_" + now.strftime("%d-%m-%Y_%Hh-%Mm-%Ss") + ".txt";
    file = open(fname, "a")
    for line in liste:
        file.write(line + '\n');
    print('|--------------------------------------------------------------------------\n'
          '|Fichier créé avec succès');

def printLines(liste):
    print('|--------------------------------------------------------------------------\n')
    for line in liste:
        print('|' + line);

def getFiles():
    for file in glob.glob(PATHLOGS + "*.log"):
        txtfiles.append(file)

def getStats(fichiers, player, printmode):
    morts = getMorts(txtfiles, player, 2);
    kills = getKills(txtfiles, player, 2);
    messages = getMessages(txtfiles, player, 2);
    if kills != 0:
        KDR = round(kills/morts, 2);
    else:
        KDR = 0.0;
    print('|--------------------------------------------------------------------------\n'
          '|Statistiques de ' + player + ' dans les fichiers log:\n'
          '|--------------------------------------------------------------------------\n'
          '|Kills : ' + str(kills) + '\t\t Morts : ' + str(morts) + '\t\tKDR : ' + str(KDR)+ '\n'
          '|Messages: ' + str(messages)
          );

def outMode():
    while 1==1:
        entryoutputmode = input('Mode de sortie: 0 - Console | 1 - Fichier (dossier /output): ');
        if re.search('[0-1]', entryoutputmode):
            outputmode = int(entryoutputmode)
            return outputmode
            break;
        else:
            print('|--------------------------------------------------------------------------\n' +
                  '|Entrez une valeur valide');

def main():
    while 1==1:
        entry = '';
        mode = 0;
        entry = input('|--------------------------------------------------------------------------\n' +
              '|Choisir le mode de recherche:\n| 1 - Activité | 2 - Mort | 3 - Kill | 4 - Statistiques | 5 - Messages | 6 - Item/Stockage/ID | 7 - Dégats\n');
        if re.search('[1-7]', entry):
            mode = int(entry);
        if mode != 0:
            getFiles();
            if mode == 1:
                getActivity(txtfiles, input("Entrez le nom d'un personnage ou d'un NPC: "), outMode());
            elif mode == 2:
                getMorts(txtfiles, input("Entrez le nom d'un personnage ou d'un NPC: "), outMode());
            elif mode == 3:
                getKills(txtfiles, input("Entrez le nom d'un personnage ou d'un NPC: "), outMode());
            elif mode == 4:
                getStats(txtfiles, input("Entrez le nom d'un personnage ou d'un NPC: "), 0);
            elif mode == 6:
                getActivity(txtfiles, input("Entrez l'identifiant ou le nom d'un item ou d'un stockage: "), outMode());
            elif mode == 5:
                getMessages(txtfiles, input("Entrez le nom d'un personnage: "), outMode());
            elif mode == 7:
                getDamage(txtfiles, input("Entrez le nom d'un personnage ou d'un NPC: "), outMode());
        elif mode == 0:
            print('|--------------------------------------------------------------------------\n' +
                  '|Entrez une valeur valide');

if __name__ == '__main__':
    main()
