import os
import sqlite3
from http.server import SimpleHTTPRequestHandler, HTTPServer
import cgi

# Dossier pour stocker les fichiers reçus
data_folder = "server_files"
os.makedirs(data_folder, exist_ok=True)

class FileServerHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        """Gérer l'upload de fichiers."""
        if self.path == '/upload':
            # Parse les données multipart/form-data
            content_type, pdict = cgi.parse_header(self.headers['Content-Type'])
            if content_type != 'multipart/form-data':
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Type de contenu non support\u00e9")
                return
            
            pdict['boundary'] = pdict['boundary'].encode()
            pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
            fields = cgi.parse_multipart(self.rfile, pdict)

            if 'file' in fields:
                uploaded_file = fields['file'][0]
                filename = fields['file'][1].decode('utf-8')  # Nom du fichier envoyé
                filepath = os.path.join(data_folder, filename)

                # Créer les répertoires nécessaires
                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                with open(filepath, "wb") as f:
                    f.write(uploaded_file)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Fichier upload\u00e9 avec succ\u00e8s")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Pas de fichier trouv\u00e9 dans la requ\u00eate")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint non trouv\u00e9")

    def do_GET(self):
        """Gérer le téléchargement de fichiers."""
        parsed_path = self.path.split('/')
        if len(parsed_path) > 1 and parsed_path[1] == 'files':
            filename = '/'.join(parsed_path[2:])
            filepath = os.path.join(data_folder, filename)
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header("Content-Type", 'application/octet-stream')
                self.send_header("Content-Length", os.path.getsize(filepath))
                self.end_headers()
                with open(filepath, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Fichier non trouv\u00e9")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint non trouv\u00e9")

    def combine_db_files(self):
        """Combiner les fichiers .db sans doublon."""
        combined_db_path = os.path.join(data_folder, "combined.db")
        conn = sqlite3.connect(combined_db_path)
        cursor = conn.cursor()

        # Créer une table temporaire pour stocker les données combinées
        cursor.execute("CREATE TABLE IF NOT EXISTS combined_data (id INTEGER PRIMARY KEY, data TEXT)")

        for root, dirs, files in os.walk(data_folder):
            for file in files:
                if file.endswith(".db"):
                    file_path = os.path.join(root, file)
                    with sqlite3.connect(file_path) as db_conn:
                        db_cursor = db_conn.cursor()
                        db_cursor.execute("SELECT * FROM data")
                        rows = db_cursor.fetchall()
                        for row in rows:
                            cursor.execute("INSERT OR IGNORE INTO combined_data (id, data) VALUES (?, ?)", row)

        conn.commit()
        conn.close()

if __name__ == "__main__":
    # Configuration du serveur
    server_address = ('', 5000)  # Écoute sur toutes les interfaces, port 5000
    httpd = HTTPServer(server_address, FileServerHandler)
    print("Serveur démarré sur le port 5000...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Arrêt du serveur.")
        httpd.server_close()