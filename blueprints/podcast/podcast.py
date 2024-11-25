from config import *

podcast_bp = Blueprint("podcast", __name__, template_folder="templates")


def get_db_connection():
    conn = sqlite3.connect(DB_IATITUS)
    conn.row_factory = sqlite3.Row
    return conn


@podcast_bp.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT PkIdArq AS id, TituloArq as title FROM TBArquivo WHERE FlgResumoArq = 0")
    pdfs = cursor.fetchall()

    conn.close()

    return render_template('podatituspg2.html', pdfs=pdfs)


@podcast_bp.route('/generate_podcast', methods=['POST'])
def generate_podcast_route():
    selected_ids = request.form.getlist('selected_pdfs')
    selected_ids = [int(id) for id in selected_ids]

    conn = get_db_connection()
    pdf_files = get_pdfs_content(conn, selected_ids)
    conn.close()

    # Configuração do podcast
    podcast_config = {
        'word_count': 800,
        'conversation_style': ['Engajante', 'Ritmo acelerado', 'Entusiástico', 'Educacional'],
        'roles_person1': 'Entrevistador',
        'roles_person2': 'Especialista no assunto discutido',
        'dialogue_structure': ['Introdução do tópico', 'Sumário de pontos chaves', 'Discussão', 'Perguntas e respostas',
                               'Mensagem de despedida'],
        'podcast_name': 'Pod Atitus',
        'podcast_tagline': 'A sua dose de conhecimento gerada por IA',
        'output_language': 'Português',
        'user_instructions': 'Faça educacional e engajante',
        'engagement_techniques': ['Rhetorical Questions', 'Personal Testimonials', 'Quotes', 'Anecdotes', 'Analogies',
                                  'Humor'],
        'creativity': 0.7,
        'text_to_speech': {
            'temp_audio_dir': './data/audio',
            'ending_message': "Obrigado por ouvir a mais um episódio. Seguimos à sua disposição para lhe auxiliar em todas as suas dúvidas.",
            'default_tts_model': 'openai',
            'openai': {
                'default_voices': {'question': 'nova', 'answer': 'onyx'},
                'model': 'tts-1-hd'
            },
            'audio_format': 'mp3'
        }
    }

    # Gerar o podcast
    audio_file_path = generate_podcast(urls=pdf_files, conversation_config=podcast_config, tts_model="elevenlabs")

    # Verificar se o arquivo de áudio foi gerado
    if not os.path.exists(audio_file_path):
        print("_______________________________________________________________________________________")
        print("Erro: Arquivo de áudio não foi gerado.")
        return "Erro ao gerar o podcast.", 500

    # Definir o caminho de destino
    podcast_file_path = os.path.join('static', 'podcasts', 'podcast.mp3')
    os.makedirs(os.path.dirname(podcast_file_path), exist_ok=True)

    # Copiar o arquivo gerado para o diretório estático
    shutil.copyfile(audio_file_path, podcast_file_path)

    # Redirecionar para a página de reprodução do podcast
    return redirect(url_for('podcast.play_podcast'))


@podcast_bp.route('/play_podcast')
def play_podcast():
    # Renderizar um template que inclui um player de áudio
    return render_template('podatituspg3.html')
