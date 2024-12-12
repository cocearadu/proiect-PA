from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

# Crearea unui dicționar gol pentru orar
orar_data = {}

# Functia care permite introducerea orarului pentru o zi
def introducere_orar(zi):
    materii = []
    print(f"Introduceti orarul pentru {zi}:")
    while True:
        materie = input(f"Introduceti materia pentru {zi} (sau apasati Enter pentru a incheia): ")
        if materie == "":
            break  # Ieșim din buclă dacă nu se introduce nimic
        materii.append(materie)
    orar_data[zi] = materii  # Salvăm orarul pentru ziua respectivă

# Introducerea orarului pentru fiecare zi a săptămânii
introducere_orar('Luni')
introducere_orar('Marti')
introducere_orar('Miercuri')
introducere_orar('Joi')
introducere_orar('Vineri')

# Verificare (afisare orar complet)
print("\nOrar complet:")
for zi, materii in orar_data.items():
    print(f"{zi}: {', '.join(materii)}")


# Crearea documentului PDF
pdf_file_path = 'orar_scolar_fara_diacritice.pdf'
pdf = SimpleDocTemplate(pdf_file_path, pagesize=landscape(A4))

# Crearea stilurilor pentru text
styles = getSampleStyleSheet()

# Definirea datelor pentru tabel
header = ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri']
data = [header]

# Completarea datelor în funcție de orar
max_rows = max([len(orar_data[day]) for day in orar_data])
for i in range(max_rows):
    row = []
    for day in header:
        try:
            # Eliminare diacritice
            row.append(orar_data[day][i].replace('Ș', 'S').replace('Ț', 'T').replace('Ă', 'A').replace('Î', 'I').replace('Â', 'A').replace('ș', 's').replace('ț', 't').replace('ă', 'a').replace('î', 'i').replace('â', 'a'))
        except IndexError:
            row.append('')  # Dacă nu există materie pentru această oră, lăsăm celula goală
    data.append(row)

# Crearea tabelului
table = Table(data, colWidths=[55*mm]*5, rowHeights=10*mm)

# Stilizarea tabelului
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

# Adăugarea conținutului în PDF
elements = [Paragraph('Orar Scolar', styles['Title']), table]

# Generarea PDF-ului
pdf.build(elements)

print(f"PDF-ul a fost generat: {pdf_file_path}")
