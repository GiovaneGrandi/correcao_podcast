from config import *

chatbot_bp = Blueprint("chatbot", __name__, template_folder="templates")


@chatbot_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('chatbot.html')


@chatbot_bp.route('/process', methods=['POST'])
def process_input():
    # Recebe o input do JavaScript
    data = request.json
    userQuestion = data.get('question')

    conn = sqlite3.connect(DB_IATITUS)
    cursor = conn.cursor()
    cursor.execute(f"SELECT ConteudoArq FROM TBArquivo WHERE PkIdArq = 5")

    contexto = cursor.fetchone()

    print(contexto)

    response_text = askQuestionFromPdf(contexto, userQuestion)

    return jsonify({'result': response_text})