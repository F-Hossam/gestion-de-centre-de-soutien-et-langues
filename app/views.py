from flask import Blueprint, render_template, request, redirect, url_for
from .models import * 

views = Blueprint('views',__name__)

@views.route("/")
def index():    
    return render_template("index.html")

@views.route("/inscription", methods=['GET','POST'])
def inscription():
    if request.method=='POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        datenaissance = request.form['datenaissance']
        niveau = request.form['niveau']
        add(nom, prenom, datenaissance, niveau)
        return redirect(url_for('views.formation'))

    return render_template("inscription.html")

@views.route("/seance", methods=['GET','POST'])
def seance():
    if request.method == "POST":
        num = int(request.form.get('groupe-loop'))
        first_index = int(request.form.get('first-etudiant-index'))
        seance = int(request.form.get('num-seance'))
        today = get_today_reg()
        etudiant_status = []
        for i in range(0+first_index,num+first_index):
            name = request.form.get(f'etudiant-name-{i}')
            present = int(request.form.get(f'etudiant-present-{i}'))
            payer = int(request.form.get(f'payer-etudiant-{i}'))
            etudiant_status.append([name,seance,present,payer])
            assister(name,present,seance,today)
            gestion_presence(name,seance,payer)

    seances = generate_seance()
    formations = [formation_de_groupe(seance[1]) for seance in seances]
    etudiants = [etudiants_de_groupe(seance[1]) for seance in seances]
    soldes = []
    m = []
    i = 0
    k = 0
    for etudiant in etudiants:
        f = formations[i]
        soldes.append([solde_de_etudiant(e,f) for e in etudiant])
        m.append([i for i in range(1+k,len(etudiant)+1+k)])
        i += 1
        k += len(etudiant)
    return render_template("seance.html", data = zip(seances, formations, etudiants, soldes, m))

@views.route("/formation", methods=['GET','POST'])
def formation():        
    if request.method=="POST":
        formation = request.form.get('formation')
        is_test = (request.form.get('test') == 'true')
        name = request.form.get('etudiant_name').split(' ')
        inscription_complet(formation,name[1],name[0],is_test)

    etudiants = list(generate_etudiants())
    niveaux = list(generate_niveau())
    autre_formations = list(generate_autre_formations())
    formations_etudiants = [list(generate_formations(etudiant[1], etudiant[0])) for etudiant in etudiants]
    formations_chaque_etudiant = []
    for formation in formations_etudiants:
        if formation == autre_formations:
            formations_chaque_etudiant.append(formation)
        else:
            formations_chaque_etudiant.append(formation+autre_formations)
    
    return render_template("formation.html", data=zip(etudiants,formations_chaque_etudiant,niveaux))

@views.route("/groupe", methods=['GET','POST'])
def groupe():
    if request.method == "POST":
        choice = request.form.get('seance').split(' ')
        jour = choice[0]
        heur = choice[1]
        code_groupe = request.form.get('groupe_code')
        affecter_a_seance(code_groupe,jour,heur)

    groupes, formations = generate_full_groupes()
    seances_chaque_groupe = [seance_disponible(groupe[0]) for groupe in groupes]
    return render_template("groupe.html", data = zip(groupes, formations, seances_chaque_groupe))

@views.route("/etudiant")
def etudiant():
    etudiants,formation_groupe = generate_info_etudiants()
    return render_template("etudiant.html", data = zip(etudiants,formation_groupe))

@views.route("/home")
def home():
    return render_template("home.html")