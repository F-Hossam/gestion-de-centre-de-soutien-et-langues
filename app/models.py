from . import mysql
from datetime import date, datetime
import locale

def add(nom, prenom, date_naiss, niveau):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO etudiant (nom, prenom, date_naiss, nive) VALUES (%s, %s, %s, %s)", (nom, prenom, date_naiss, niveau))
    mysql.connection.commit()
    cur.close()

def generate_etudiants():
    cur = mysql.connection.cursor()
    cur.execute("SELECT prenom, nom FROM etudiant ORDER BY id_etudiant DESC")
    etudiants = cur.fetchall()
    return etudiants

def generate_info_etudiants():
    cur = mysql.connection.cursor()
    cur.execute("SELECT prenom, nom, niveau FROM etudiant")
    etudiants = cur.fetchall()
    cur.execute("SELECT id_etudiant FROM etudiant")
    id_etudiants = cur.fetchall()
    formation_groupe = []
    
    for id_etudiant in id_etudiants:
        cur.execute("SELECT nom ,codeg from formation,groupe  WHERE num=idf and idf in  (SELECT idf FROM  groupe WHERE codeg in (SELECT codeg FROM grpetudiant WHERE id_etudianti = %s)) and codeg in (SELECT codeg FROM grpetudiant WHERE id_etudianti = %s)  ",(id_etudiant,id_etudiant))
        groupes = cur.fetchall()
        formation_groupe.append(groupes)
        
    cur.close()
    return (etudiants,formation_groupe)

def generate_formations(nom: str, prenom: str):
    cur = mysql.connection.cursor()
    cur.execute("SELECT nom FROM formation WHERE niveau_f in (SELECT niveau FROM etudiant WHERE nom=%s AND prenom=%s)", (nom, prenom))
    formations = cur.fetchall()
    cur.close()
    return formations

def generate_autre_formations():
    cur = mysql.connection.cursor()
    cur.execute("SELECT nom FROM formation WHERE niveau_f=%s", ('autre',))
    formations = cur.fetchall()
    cur.close()
    return formations

def inscription_complet(formation,nom,prenom,test):
    id_etudiant,id_departement = add_formation(formation,nom,prenom,test)
    somme = somme_a_payer(id_departement,test)
    payer(id_etudiant,id_departement,somme)
    affecter_au_groupe((f'{formation}',),id_etudiant)

def generate_niveau():
    cur = mysql.connection.cursor()
    cur.execute("SELECT niveau FROM etudiant ORDER BY id_etudiant DESC")
    niveaux = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return niveaux

#fonctions auxiliaires

def add_formation(formation,nom,prenom,test):
    cur = mysql.connection.cursor()
    cur.execute("SELECT num FROM formation WHERE nom = %s",((f'{formation}',)))
    id_formation = cur.fetchone()
    cur.execute("SELECT idep FROM formation WHERE nom=%s",((f'{formation}',)))
    id_departement = cur.fetchone()
    cur.execute("SELECT id_etudiant FROM etudiant WHERE nom=%s AND prenom=%s",(nom,prenom))
    id_etudiant = cur.fetchone()
    cur.execute("INSERT INTO inscription (id_etudianti, id_departementi,id_form,date_insci,test) VALUES (%s, %s, %s, %s, %s)",(id_etudiant,id_departement,id_formation,get_today_reg(),test))
    mysql.connection.commit()
    cur.close()
    return (id_etudiant,id_departement)
    
def get_today():
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    return date.today().strftime('%A')

def get_time():
    return datetime.now().strftime('%I:%M')

def generate_full_groupes():
    cur = mysql.connection.cursor()
    cur.execute("select codeg, idf FROM groupe WHERE codeg IN ( SELECT codeg FROM grpetudiant GROUP BY codeg HAVING COUNT(id_etudianti) >= 4) AND codeg NOT IN (SELECT grp FROM seance)")
    groupes= cur.fetchall()

    formations = (generate_formation(groupe[1]) for groupe in groupes)
    mysql.connection.commit()
    cur.close()
    return (groupes,formations)

def generate_formation(idf):
    cur = mysql.connection.cursor()
    cur.execute("SELECT nom, niveau_f FROM formation WHERE num = %s",(f'{idf}',))
    formation = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return formation

def affecter_au_groupe(formation,id_etudiant):
    cur = mysql.connection.cursor()
    #selectionner le numero de la formation
    cur.execute("SELECT niveau FROM etudiant WHERE id_etudiant = %s",(id_etudiant))
    niveau = cur.fetchone()
    autre = generate_autre_formations()
    if formation in autre: niveau_f = ('autre',)
    else: niveau_f = niveau
    cur.execute("SELECT num FROM formation WHERE nom = %s AND niveau_f = %s",(formation,niveau_f))
    id_formation = cur.fetchone()
    #affecter l'étudiant au groupe
    code_groupe = groupe_de_formation(id_formation)  #none fle cas dial affectation
    cur.execute("INSERT INTO grpetudiant (id_etudianti, codeg) VALUES (%s, %s)",(id_etudiant,code_groupe))
    mysql.connection.commit()
    cur.close()

def payer(id_etudiant,id_departement,somme):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE inscription SET solde = %s WHERE id_etudianti = %s and id_departementi = %s",(somme,id_etudiant,id_departement))
    mysql.connection.commit()
    cur.close()

def somme_a_payer(id_departement,test):
    if test == False:
        return 300
    elif test == True and id_departement==1:
        return 400
    else:
        return 1600
    
def creer_nouveau_groupe(id_formation):
    cur = mysql.connection.cursor()
    cur.execute("SELECT matricule FROM enseignent WHERE numf = %s",(id_formation))
    matricule = cur.fetchone()
    cur.execute("INSERT INTO groupe (idf,matr) VALUES (%s,%s)",(id_formation,matricule))
    cur.execute("SELECT codeg FROM groupe WHERE idf = %s",(id_formation))
    code_groupe = cur.fetchall()[-1]
    mysql.connection.commit()
    cur.close()
    return code_groupe

def groupe_de_formation(id_formation):
    cur = mysql.connection.cursor()
    #déterminer le groupe convenable
    cur.execute("SELECT codeg FROM groupe WHERE idf = %s",(id_formation))
    a = cur.fetchall()
    if len(a)==0 and nombre_groupes() < 42:
        code_groupe = creer_nouveau_groupe(id_formation)
    else:
        cur.execute("SELECT codeg FROM grpetudiant WHERE codeg IN (SELECT codeg FROM groupe WHERE idf = %s) GROUP BY codeg HAVING COUNT(id_etudianti) < 8",(id_formation))
        code_groupe = cur.fetchone()
        if code_groupe == None and nombre_groupes() < 42:
            code_groupe = creer_nouveau_groupe(id_formation)

    mysql.connection.commit()
    cur.close()
    return code_groupe

def nombre_groupes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(codeg) FROM groupe")
    number = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return number[0]

def affecter_a_seance(code_groupe, jour, heure):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO seance (jour, heure, grp) VALUES (%s, %s, %s)", (jour, heure, code_groupe))
    mysql.connection.commit()
    cur.close()

def seance_disponible(code_groupe):
    cur = mysql.connection.cursor()
    cur.execute("SELECT jour FROM seance GROUP BY jour HAVING COUNT(grp) = 9") #les jours free
    jours_full = cur.fetchall()
    jours_reg = (('lundi',), ('mardi',), ('mercredi',), ('jeudi',), ('vendredi',), ('samedi',), ('dimanche',))
    jours = [jour for jour in jours_reg if jour not in jours_full]
    cur.execute("SELECT idf FROM groupe WHERE codeg = %s", (f'{code_groupe}',)) #formation du groupe
    idf = cur.fetchone() 

    seances_dispo = []
    heures = (('6:00',),('8:00',),('10:00',))
    for jour in jours :
        for heure in heures :
            cur.execute("SELECT COUNT(grp) FROM seance WHERE heure = %s AND jour = %s",(heure, jour))
            num_grp = cur.fetchone()
            if num_grp[0] < 4:
                cur.execute("SELECT COUNT(grp) FROM seance WHERE heure = %s AND jour = %s AND grp NOT IN (SELECT codeg FROM groupe WHERE idf = %s)", (heure,jour,idf))
                num_grp_autre = cur.fetchone()
                if num_grp == num_grp_autre:
                    seances_dispo.append((jour,heure))
                
    mysql.connection.commit()
    cur.close()
    return seances_dispo

def formation_de_groupe(code_groupe):
    cur = mysql.connection.cursor()
    cur.execute("SELECT idf FROM groupe WHERE codeg = %s",((f"{code_groupe}",)))
    idf = cur.fetchone()
    formation = generate_formation(idf[0])[0]
    mysql.connection.commit()
    cur.close()
    return formation

def nom_prenom_etudiant(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT nom, prenom FROM etudiant WHERE id_etudiant = %s", ((f"{id}",)))
    etudiant = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return etudiant

def solde_de_etudiant(etudiant, formation):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_etudiant FROM etudiant WHERE nom = %s AND prenom = %s",(etudiant[0],etudiant[1]))
    id_etudiant = cur.fetchone()
    cur.execute("SELECT num FROM formation WHERE nom = %s",((f"{formation}",)))
    id_formation = cur.fetchone()
    cur.execute("SELECT solde FROM inscription WHERE id_etudianti = %s AND id_form = %s",(id_etudiant,id_formation))
    solde = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return solde

def etudiants_de_groupe(code_groupe):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_etudianti FROM grpetudiant WHERE codeg = %s",((f"{code_groupe}",)))
    id_etudiants = cur.fetchall()
    etudiants = [nom_prenom_etudiant(id[0]) for id in id_etudiants]
    mysql.connection.commit()
    cur.close()
    return etudiants

def generate_seance():
    jour = get_today()
    heur = get_time()
    cur = mysql.connection.cursor()
    cur.execute("SELECT codee,grp FROM seance WHERE jour = %s AND heure >= %s",(jour, heur))
    seances = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return seances

def assister(etudiant : str,presence, seance : int, day):
    cur = mysql.connection.cursor()
    id_etudiant = get_id_etudiant(etudiant)
    cur.execute("INSERT INTO assister (id_etudianta,codeea,presence,datea) VALUES (%s,%s,%s,%s)", (id_etudiant,seance,presence,day))
    mysql.connection.commit()
    cur.close()

def get_today_reg():
    return date.today()

def get_id_etudiant(etudiant : str):
    e_list = etudiant.split(' ')
    nom = e_list[1]
    prenom = e_list[0]
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_etudiant FROM etudiant WHERE nom = %s AND prenom = %s",(nom, prenom))
    id = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return id

def gestion_presence(etudiant : str, seance : int, payer:int):
    today = get_today_reg()
    cur = mysql.connection.cursor()
    id_etudiant = get_id_etudiant(etudiant)

    cur.execute("SELECT grp FROM seance WHERE codee = %s",(f'{seance}',))
    code_g = cur.fetchone()

    cur.execute("SELECT idf FROM groupe WHERE codeg = %s",(code_g))
    id_form = cur.fetchone()

    cur.execute("SELECT presence FROM assister WHERE id_etudianta = %s AND codeea = %s AND datea = %s",(id_etudiant,seance,today))
    presence = cur.fetchone()

    if presence == (0,):
        cur.execute("UPDATE grpetudiant SET consecutive_absences = consecutive_absences + 1 WHERE id_etudianti = %s AND codeg = %s",(id_etudiant,code_g))
        cur.execute("SELECT consecutive_absences FROM grpetudiant WHERE id_etudianti = %s AND codeg = %s",(id_etudiant,code_g))
        consecutive_abs = cur.fetchone()
        if consecutive_abs == (2,):
            cur.execute("SELECT solde FROM inscription WHERE id_etudianti = %s AND id_form = %s",(id_etudiant,id_form))
            student_solde = cur.fetchone()
            if student_solde == (0,):
                cur.execute("DELETE FROM grpetudiant WHERE id_etudianti = %s AND codeg = %s",(id_etudiant,code_g))
                cur.execute("DELETE FROM inscription where id_etudianti = %s and id_form = %s",(id_etudiant,id_form))
            else:
                cur.execute("UPDATE inscription SET solde = solde - 150 WHERE id_etudianti = %s and id_form = %s",(id_etudiant,id_form))
                cur.execute("UPDATE grpetudiant SET consecutive_absences = 0 WHERE id_etudianti = %s AND codeg = %s",(id_etudiant,code_g))
    else:
        cur.execute("SELECT solde FROM inscription WHERE id_etudianti = %s AND id_form = %s",(id_etudiant,id_form))
        student_solde = cur.fetchone()
        print(student_solde)
        if student_solde == (0,) and payer == 1:
            cur.execute("UPDATE inscription SET solde = 150 WHERE id_etudianti = %s and id_form = %s",(id_etudiant,id_form))
        elif student_solde == (0,) and payer == 0:
            cur.execute("DELETE FROM grpetudiant WHERE id_etudianti = %s AND codeg = %s",(id_etudiant,code_g))
            cur.execute("DELETE FROM inscription where id_etudianti = %s and id_form = %s",(id_etudiant,id_form))
        else:
            cur.execute("UPDATE inscription SET solde = solde - 150 WHERE id_etudianti = %s AND id_form = %s",(id_etudiant,id_form))

    mysql.connection.commit()
    cur.close()
