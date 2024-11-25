from config import *

newdocument_bp = Blueprint("newdocument", __name__, template_folder="templates")


@newdocument_bp.route("/", methods=['GET', 'POST'])
def index():
    # Recebe o input do JavaScript
    if request.method == 'POST':

        conn = sqlite3.connect(DB_IATITUS)
        cursor = conn.cursor()

        title = request.form.get('title')
        cadeira = request.form.get('cadeira')
        file = request.files.get('file')

        if not file:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400

        file.save(SRC_RECUPERADO)

        with open(SRC_RECUPERADO, 'rb') as file:
            conteudo_binario = file.read()

            cursor.execute('''
               INSERT INTO TBArquivo (FkIdCad, TituloArq, ConteudoArq, FlgResumoArq)
               VALUES (?, ?, ?, ?)
               ''', (cadeira, title, conteudo_binario, 0))

        pdfText = extractTextFromPdf(SRC_RECUPERADO)
        finalText = summarizePdf(pdfText)

        cursor.execute(
            f"INSERT INTO TBArquivo (TituloArq, ConteudoArq, FkIdCad, FlgResumoArq) VALUES ('{title}', '{finalText}', {cadeira}, 1);")
        conn.commit()
        conn.close()

    conn = sqlite3.connect(DB_IATITUS)
    cursor = conn.cursor()

    cursor.execute("SELECT PkIdCad AS id, nomeCad AS nome FROM TBCadeira")
    cadeiras = cursor.fetchall()  # [(1, 'Categoria 1'), (2, 'Categoria 2'), ...]

    conn.close()

    return render_template('newdocument.html', cadeiras=cadeiras)